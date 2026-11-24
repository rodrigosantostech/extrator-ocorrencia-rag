"""Leitura validada do manual modular, sem indexar exemplos ou documentos históricos."""

import hashlib
import json
from pathlib import Path

INICIO = "<!-- INICIO_CONTEUDO_ORIGINAL -->\n"
FIM = "<!-- FIM_CONTEUDO_ORIGINAL -->"


def carregar_base(manifesto: Path, versao: str = "2026.3") -> dict[str, object]:
    if versao != "2026.3":
        raise ValueError("Somente o manual vigente 2026.3 está disponível.")
    dados_manifesto = manifesto.read_bytes()
    dados = json.loads(dados_manifesto.decode("utf-8"))
    if (
        not isinstance(dados, dict)
        or dados.get("formato") != "manual-modular-1"
        or dados.get("versao") != versao
    ):
        raise ValueError("Manifesto inválido ou de versão divergente.")
    itens = dados.get("documentos")
    if not isinstance(itens, list) or not itens:
        raise ValueError("Manifesto sem documentos.")
    raiz = manifesto.parent.resolve()
    documentos = []
    nomes = set()
    for item in itens:
        nome = item.get("arquivo") if isinstance(item, dict) else None
        if (
            not isinstance(nome, str)
            or Path(nome).name != nome
            or "/" in nome
            or "\\" in nome
            or not nome.endswith(".md")
            or nome in nomes
        ):
            raise ValueError("Nome de documento inválido ou duplicado no manifesto.")
        caminho = raiz / nome
        if caminho.is_symlink() or caminho.resolve().parent != raiz:
            raise ValueError("Documento fora da base autorizada.")
        bruto = caminho.read_bytes()
        digest = hashlib.sha256(bruto).hexdigest()
        if digest != item.get("sha256"):
            raise ValueError(
                "Documento diverge do hash registrado; atualize e revise o manifesto."
            )
        texto = bruto.decode("utf-8").replace("\r\n", "\n")
        if texto.count(INICIO) != 1 or texto.count(FIM) != 1:
            raise ValueError("Delimitação de conteúdo original inválida.")
        conteudo = texto.split(INICIO, 1)[1].split(FIM, 1)[0]
        if not conteudo.strip():
            raise ValueError("Documento vazio.")
        documentos.append(
            {**item, "fonte": f"{manifesto.parent.name}/{nome}", "texto": conteudo}
        )
        nomes.add(nome)
    return {
        "versao": versao,
        "sha256": hashlib.sha256(dados_manifesto).hexdigest(),
        "original_sha256": dados.get("original_sha256", "INDISPONÍVEL"),
        "manifesto": str(manifesto),
        "documentos": documentos,
    }
