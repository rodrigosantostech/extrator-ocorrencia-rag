"""Único ponto de acesso à Responses API, sem repetição automática ou log de segredos."""

import json
import time

from .config import Configuracao
from .privacidade import limpar_objeto


class ClienteOpenAI:
    def __init__(self, configuracao: Configuracao) -> None:
        self.configuracao = configuracao
        self._cliente = None
        self.chamadas: list[dict] = []

    def chamar(
        self, etapa: str, instrucoes: str, dados: str, schema: dict[str, object]
    ) -> dict[str, object] | None:
        resultado = self._chamar(etapa, instrucoes, dados, schema)
        return resultado if isinstance(resultado, dict) else None

    def chamar_texto(self, etapa: str, instrucoes: str, dados: str) -> str | None:
        resultado = self._chamar(etapa, instrucoes, dados, None)
        return resultado if isinstance(resultado, str) else None

    def _chamar(
        self,
        etapa: str,
        instrucoes: str,
        dados: str,
        schema: dict[str, object] | None,
    ) -> dict[str, object] | str | None:
        cfg = self.configuracao
        registro = {
            "etapa": etapa,
            "modelo_solicitado": cfg.modelo,
            "parametros": cfg.parametros,
            "instrucoes": instrucoes,
            "entrada": dados,
            "schema": schema,
            "status": "ERRO_TECNICO",
            "tentativa_http": False,
            "latencia_segundos": None,
            "tokens": None,
            "custo_usd_estimado": None,
        }
        self.chamadas.append(registro)
        inicio = time.perf_counter()
        try:
            from openai import OpenAI, OpenAIError

            if not cfg.chave_api.strip():
                registro["erro"] = {"tipo": "CREDENCIAL_AUSENTE"}
                return None
            if self._cliente is None:
                self._cliente = OpenAI(
                    api_key=cfg.chave_api,
                    base_url="https://api.openai.com/v1",
                    timeout=cfg.timeout_segundos,
                    max_retries=0,
                )
            registro["tentativa_http"] = True
            parametros = {
                "model": cfg.modelo,
                "instructions": instrucoes,
                "input": dados,
                **cfg.parametros,
            }
            if schema is not None:
                parametros["text"] = {
                    "format": {
                        "type": "json_schema",
                        "name": etapa,
                        "strict": True,
                        "schema": schema,
                    }
                }
            resposta = self._cliente.responses.create(**parametros)
            registro["resposta_bruta"] = limpar_objeto(
                resposta.model_dump(mode="json"), (cfg.chave_api,)
            )
            registro["saida_textual"] = limpar_objeto(
                resposta.output_text, (cfg.chave_api,)
            )
            registro["saida_mascarada"] = (
                registro["saida_textual"] != resposta.output_text
            )
            if resposta.usage:
                uso = resposta.usage
                registro["tokens"] = uso.model_dump(mode="json")
                # Preço padrão consultado em 23/11/2026; sem desconto de cache ou fatura confirmada.
                if cfg.modelo == "gpt-6-luna":
                    registro["custo_usd_estimado"] = (
                        uso.input_tokens * 0.10 + uso.output_tokens * 0.50
                    ) / 1_000_000
                    registro["formula_custo"] = (
                        "(tokens_entrada × 0,10 + tokens_saida × 0,50) / 1.000.000"
                    )
                    registro["fonte_preco"] = (
                        "https://developers.openai.com/api/docs/models/gpt-6-luna"
                    )
            if resposta.status != "completed" or not resposta.output_text:
                registro["erro"] = {"tipo": "RESPOSTA_INCOMPLETA_OU_RECUSADA"}
                return None
            if schema is None:
                registro["status"] = "OK"
                return registro["saida_textual"]
            dados_saida = json.loads(registro["saida_textual"])
            registro["status"] = "OK"
            return dados_saida
        except ImportError:
            registro["erro"] = {"tipo": "DEPENDENCIA_OPENAI_AUSENTE"}
            return None
        except (OpenAIError, TimeoutError, json.JSONDecodeError) as erro:
            # Mensagens de exceção do SDK podem conter conteúdo externo ou credenciais.
            registro["erro"] = {
                "tipo": type(erro).__name__,
                "status_http": getattr(erro, "status_code", None),
            }
            return None
        finally:
            registro["latencia_segundos"] = round(time.perf_counter() - inicio, 4)
            registro.update(limpar_objeto(registro, (cfg.chave_api,)))

    def fechar(self) -> None:
        if self._cliente is not None:
            self._cliente.close()
