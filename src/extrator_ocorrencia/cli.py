"""CLI da Rede Saúde Viva; sem argumentos, executa o fluxo simples do executável."""

import argparse
import json
import os
import sys
from pathlib import Path

from .base import carregar_base
from .config import MANUAL_PADRAO, Configuracao
from .relatorio import salvar_relatorio

LIMITE_ARQUIVO_BYTES = 24000


class ErroArgumentos(ValueError):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ErroArgumentos(
            "Argumentos inválidos. Consulte --help para a sintaxe disponível."
        )


def diagnosticar(configuracao: Configuracao) -> dict[str, object]:
    try:
        base = carregar_base(configuracao.manual)
    except (OSError, UnicodeError, ValueError):
        return {
            "status": "ERRO",
            "motivo": "Base ausente, vazia, inacessível ou divergente do manifesto.",
        }
    return {
        "status": "OK",
        "manual": str(configuracao.manual),
        "caracteres_manual": sum(len(d["texto"]) for d in base["documentos"]),
        "manual_versao": MANUAL_PADRAO,
        "manual_sha256": base["sha256"],
        "original_sha256": base["original_sha256"],
        "documentos": [
            {
                "fonte": d["fonte"],
                "sha256": d["sha256"],
                "secoes_indexadas": d["secoes_indexadas"],
                "anexo_rag": d["anexo_rag"],
            }
            for d in base["documentos"]
        ],
        "integracao_api": "DISPONIVEL_NOS_COMANDOS_EXTRAIR_E_CONSULTAR; NÃO EXECUTADA NO DIAGNÓSTICO",
        "recuperacao_rag": "DISPONIVEL_NOS_COMANDOS_EXTRAIR_E_CONSULTAR; NÃO EXECUTADA NO DIAGNÓSTICO",
        "extracao": "DISPONIVEL_NO_COMANDO_EXTRAIR; NÃO EXECUTADA NO DIAGNÓSTICO",
    }


def _adicionar_opcoes_api(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--raiz", type=Path, default=None, help="Raiz do repositório.")
    parser.add_argument(
        "--arquivo",
        type=Path,
        help="Arquivo UTF-8 com uma única entrada; não é importação de lote.",
    )
    parser.add_argument(
        "--modelo", default=None, help="Modelo a usar; o padrão vem da configuração."
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=None,
        help="Limite de tokens por resposta (padrão: 900).",
    )
    parser.add_argument(
        "--timeout-segundos",
        type=float,
        default=None,
        help="Tempo limite por chamada (padrão: 30 segundos).",
    )


def criar_parser() -> Parser:
    parser = Parser(
        description="Extrator de ocorrências e consulta RAG da Rede Saúde Viva; use somente dados sintéticos."
    )
    comandos = parser.add_subparsers(dest="comando", required=True)
    diagnostico = comandos.add_parser(
        "diagnostico", help="Verificar a leitura do manual local, sem API."
    )
    diagnostico.add_argument(
        "--raiz", type=Path, default=None, help="Raiz do repositório."
    )

    extrair = comandos.add_parser(
        "extrair",
        help="Executar o fluxo completo (v1, v2 e v3) sobre uma mensagem.",
    )
    extrair.add_argument("mensagem", nargs="?", help="Mensagem sintética.")
    _adicionar_opcoes_api(extrair)

    consultar = comandos.add_parser(
        "consultar", help="Consultar o manual com fontes recuperadas por TF-IDF."
    )
    consultar.add_argument(
        "pergunta", nargs="?", help="Pergunta sintética, entre aspas."
    )
    consultar.add_argument(
        "--manual",
        choices=(MANUAL_PADRAO,),
        default=MANUAL_PADRAO,
        help="Base vigente: manual modular 2026.3.",
    )
    consultar.add_argument(
        "--somente-recuperar",
        action="store_true",
        help="Recuperar trechos sem credencial nem API.",
    )
    _adicionar_opcoes_api(consultar)
    return parser


def _erro_tecnico(erro: Exception) -> dict[str, object]:
    # Não ecoar conteúdo externo nem mensagem de exceção que possa conter segredo.
    return {
        "status": "ERRO_TECNICO",
        "motivo": "Não foi possível ler ou validar os argumentos, a configuração ou a base.",
        "erro_tipo": type(erro).__name__,
    }


def _ler_entrada(texto: str | None, arquivo: Path | None) -> str:
    if bool(texto) == bool(arquivo):
        raise ErroArgumentos("Informe o texto ou --arquivo, exclusivamente.")
    if not arquivo:
        return texto
    if arquivo.stat().st_size > LIMITE_ARQUIVO_BYTES:
        raise ValueError("Arquivo de entrada acima do limite de 24.000 bytes.")
    return arquivo.read_text(encoding="utf-8-sig")


def _configuracao_api(args: argparse.Namespace, *, com_api: bool) -> Configuracao:
    if args.max_output_tokens is not None and args.max_output_tokens <= 0:
        raise ValueError("O limite de tokens deve ser maior que zero.")
    if args.timeout_segundos is not None and args.timeout_segundos <= 0:
        raise ValueError("O timeout deve ser maior que zero.")
    return Configuracao.carregar(
        args.raiz,
        com_api=com_api,
        modelo=args.modelo,
        max_output_tokens=args.max_output_tokens,
        timeout_segundos=args.timeout_segundos,
    )


def _executar_extracao(cfg: Configuracao, mensagem: str) -> tuple[dict, int]:
    from .extracao import extrair

    resultado = extrair(cfg, mensagem)
    return resultado, 1 if resultado["status"] == "ERRO_TECNICO" else 0


def _executar_comando(args: argparse.Namespace) -> tuple[Configuracao, dict, int]:
    cfg = Configuracao.carregar(args.raiz)
    if args.comando == "diagnostico":
        resultado = diagnosticar(cfg)
        return cfg, resultado, 0 if resultado["status"] == "OK" else 1
    if args.comando == "extrair":
        mensagem = _ler_entrada(args.mensagem, args.arquivo)
        cfg = _configuracao_api(args, com_api=True)
        return (cfg, *_executar_extracao(cfg, mensagem))

    from .assistente import consultar

    pergunta = _ler_entrada(args.pergunta, args.arquivo)
    cfg = _configuracao_api(args, com_api=not args.somente_recuperar)
    resultado = consultar(
        cfg,
        pergunta,
        versao=args.manual,
        somente_recuperar=args.somente_recuperar,
    )
    return cfg, resultado, 1 if resultado["status"] == "ERRO_TECNICO" else 0


def _registrar(
    cfg: Configuracao, resultado: dict, comando: str, retorno: int
) -> tuple[int, dict[str, object]]:
    try:
        registro, html_path, json_path = salvar_relatorio(cfg, resultado, comando)
    except (OSError, ValueError):
        return 1, {
            "status": "ERRO_TECNICO",
            "motivo": "Não foi possível gravar o relatório local. Verifique as permissões de results/.",
        }
    # Auditoria extensa fica nos arquivos; o terminal não mostra prompts internos.
    return retorno, {
        "status": registro["resultado"]["status"],
        "resultado": {
            k: v for k, v in registro["resultado"].items() if k != "chamadas"
        },
        "relatorio_html": str(html_path),
        "registro_json": str(json_path),
    }


def executar(argumentos: list[str]) -> tuple[int, dict[str, object]]:
    cfg = Configuracao.carregar()
    comando, retorno = "argumentos", 1
    try:
        args = criar_parser().parse_args(argumentos)
        comando = args.comando
        cfg, resultado, retorno = _executar_comando(args)
    except SystemExit as erro:
        resultado = {
            "status": "AJUDA" if erro.code == 0 else "ERRO_TECNICO",
            "motivo": "Consulta à ajuda do comando.",
        }
        retorno = 0 if erro.code == 0 else 1
    except (ValueError, OSError, UnicodeError) as erro:
        resultado = _erro_tecnico(erro)
    return _registrar(cfg, resultado, comando, retorno)


def _aguardar_enter() -> None:
    try:
        input("\nPressione ENTER para fechar...")
    except (EOFError, KeyboardInterrupt):
        pass


def _resumir(saida: dict[str, object]) -> None:
    resultado = saida.get("resultado", {})
    print(f"\nStatus geral: {saida['status']}")
    for item in resultado.get("resultados", []):
        print(f"- {item['versao']}: {item['status']}")
    if "CREDENCIAL_AUSENTE" in resultado.get("alertas", []):
        print(
            "Chave da API ausente: defina OPENAI_API_KEY ou crie um .env ao lado do programa."
        )
    if "relatorio_html" in saida:
        print(f"Relatório: {saida['relatorio_html']}")
    else:
        print(saida.get("motivo", "Falha ao gerar o relatório."))


def _abrir_relatorio(caminho: str) -> None:
    try:
        os.startfile(caminho)
    except (AttributeError, OSError):
        print("Abra o relatório pelo caminho informado acima.")


def fluxo_simples() -> int:
    print("Extrator de Ocorrências — Rede Saúde Viva")
    print("Use somente dados sintéticos.\n")
    try:
        mensagem = input("Digite o prompt: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada cancelada.")
        return 1
    if not mensagem:
        print("Nenhum prompt informado.")
        _aguardar_enter()
        return 2

    print("\nProcessando: segurança, recuperação no manual e extração v1/v2/v3...")
    cfg = Configuracao.carregar()
    retorno = 1
    try:
        cfg = Configuracao.carregar(com_api=True)
        resultado, retorno = _executar_extracao(cfg, mensagem)
    except (ValueError, OSError, UnicodeError) as erro:
        resultado = _erro_tecnico(erro)
    retorno, saida = _registrar(cfg, resultado, "extrair", retorno)
    _resumir(saida)
    if "relatorio_html" in saida:
        _abrir_relatorio(saida["relatorio_html"])
    if retorno != 0:
        _aguardar_enter()
    return retorno


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stdin):
        codificacao = (getattr(stream, "encoding", "") or "").lower().replace("_", "-")
        if hasattr(stream, "reconfigure") and codificacao not in {"utf-8", "utf8"}:
            stream.reconfigure(encoding="utf-8")
    argumentos = argv if argv is not None else sys.argv[1:]
    if not argumentos:
        return fluxo_simples()
    retorno, saida = executar(argumentos)
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    return retorno
