"""Diagnóstico local da estrutura; não executa extração nem chamadas à API."""

import argparse
import json
from pathlib import Path

from .config import Configuracao


def diagnosticar(configuracao: Configuracao) -> dict[str, object]:
    try:
        texto = configuracao.manual.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return {
            "status": "ERRO",
            "motivo": "Manual ausente, inacessível ou com codificação UTF-8 inválida.",
        }
    if not texto.strip():
        return {"status": "ERRO", "motivo": "O manual está vazio."}
    return {
        "status": "OK",
        "manual": str(configuracao.manual),
        "caracteres_manual": len(texto),
        "integracao_api": "PENDENTE",
        "recuperacao_rag": "PENDENTE",
        "extracao": "PENDENTE",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Estrutura local do extrator de ocorrências.")
    subcomandos = parser.add_subparsers(dest="comando", required=True)
    diagnostico = subcomandos.add_parser("diagnostico", help="Verificar a leitura do manual local.")
    diagnostico.add_argument("--raiz", type=Path, default=None, help="Raiz do repositório; padrão: diretório atual.")
    argumentos = parser.parse_args(argv)
    resultado = diagnosticar(Configuracao.carregar(argumentos.raiz))
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if resultado["status"] == "OK" else 1
