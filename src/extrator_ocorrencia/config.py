"""Configuração centralizada; leitura restrita do .env, sem executar seu conteúdo."""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

MODELO_PADRAO = "gpt-6-luna"
MANUAL_PADRAO = "2026.3"


def ler_ambiente(raiz: Path) -> dict[str, str]:
    valores = {}
    caminho = raiz / ".env"
    if caminho.exists():
        for linha in caminho.read_text(encoding="utf-8-sig").splitlines():
            nome, separador, valor = (
                linha.strip().removeprefix("export ").partition("=")
            )
            if separador and nome.strip() in {"OPENAI_API_KEY", "OPENAI_MODEL"}:
                valor = valor.strip()
                if valor.startswith(('"', "'")):
                    delimitador = valor[0]
                    fim = valor.find(delimitador, 1)
                    if fim < 0 or (
                        valor[fim + 1 :].strip()
                        and not valor[fim + 1 :].strip().startswith("#")
                    ):
                        raise ValueError("Formato de configuração não suportado.")
                    valor = valor[1:fim]
                else:
                    valor = valor.split(" #", 1)[0].strip()
                valores[nome.strip()] = valor
    for nome in ("OPENAI_API_KEY", "OPENAI_MODEL"):
        if nome in os.environ:
            valores[nome] = os.environ[nome]
    return valores


@dataclass(frozen=True)
class Configuracao:
    raiz: Path
    modelo: str = MODELO_PADRAO
    chave_api: str = field(default="", repr=False)
    max_output_tokens: int = 900
    timeout_segundos: float = 30.0

    @classmethod
    def carregar(
        cls,
        raiz: Path | str | None = None,
        *,
        com_api: bool = False,
        modelo: str | None = None,
        max_output_tokens: int | None = None,
        timeout_segundos: float | None = None,
    ) -> "Configuracao":
        raiz_padrao = (
            Path(sys.executable).resolve().parent
            if getattr(sys, "frozen", False)
            else Path.cwd()
        )
        caminho = Path(raiz if raiz is not None else raiz_padrao).resolve()
        ambiente = ler_ambiente(caminho) if com_api else {}
        return cls(
            caminho,
            modelo=modelo or ambiente.get("OPENAI_MODEL", MODELO_PADRAO),
            chave_api=ambiente.get("OPENAI_API_KEY", ""),
            max_output_tokens=(
                max_output_tokens if max_output_tokens is not None else 900
            ),
            timeout_segundos=(
                timeout_segundos if timeout_segundos is not None else 30.0
            ),
        )

    @property
    def documentos(self) -> Path:
        diretorio_temporario = getattr(sys, "_MEIPASS", None)
        if diretorio_temporario:
            documentos_incluidos = Path(diretorio_temporario) / "data" / "documents"
            if documentos_incluidos.is_dir():
                return documentos_incluidos
        return self.raiz / "data" / "documents"

    @property
    def manual(self) -> Path:
        return self.caminho_manual(MANUAL_PADRAO)

    def caminho_manual(self, versao: str) -> Path:
        if versao == "2026.3":
            return self.documentos / "manual_v2026_3" / "manifesto.json"
        raise ValueError("Versão de manual não suportada.")

    @property
    def resultados(self) -> Path:
        return self.raiz / "results"

    @property
    def parametros(self) -> dict[str, object]:
        return {
            "reasoning": {"effort": "none"},
            "max_output_tokens": self.max_output_tokens,
            "store": False,
        }
