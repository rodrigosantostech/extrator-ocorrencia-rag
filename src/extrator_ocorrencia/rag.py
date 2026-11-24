"""TF-IDF lexical com cosseno, IDs estáveis e política de privacidade obrigatória."""

import math
import re
from collections import Counter
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from .base import carregar_base
from .privacidade import normalizar

PARADAS = set(
    "a o as os de da do das dos e em na no nas nos para por com um uma que qual quais como quando quanto sobre ao aos se ser esta este esse essa voce eu me meu minha fazer devo deve sao mais tem ha foi isso".split()
)


def termos(texto: str) -> list[str]:
    texto = normalizar(texto)
    texto = re.sub(r"\bl[0o]ja\s*0?(\d+)\b", r"loja \1", texto)
    texto = re.sub(r"\blj\s*0?(\d+)\b", r"loja \1", texto)
    texto = re.sub(r"\b([a-z]{2,3})-(\d{2})\b", r"\1\2", texto)
    return [
        t
        for t in re.findall(r"\b\w+\b", texto)
        if t not in PARADAS and (len(t) > 1 or t.isdigit())
    ]


@dataclass(frozen=True)
class Trecho:
    id: str
    titulo: str
    texto: str
    fonte: str
    versao: str
    sha256: str
    proposta_pendente: bool = False
    pontuacao: float = 0.0
    obrigatorio: bool = False
    secao: str = ""

    def registro(self) -> dict[str, object]:
        return asdict(self)


def trechos_secoes_operacionais(
    conteudo: str, *, exigir_completude: bool = True
) -> list[tuple[str, str, str, str]]:
    """Amplia o anexo com texto literal; exclui saídas de exemplo e gabaritos."""
    partes = []
    selecionadas = {2, 4, 5, 6, 7, 8, 9, 12, 16}
    for secao in re.finditer(
        r"^## (\d+)\. ([^\n]+)\n(.*?)(?=^## |\Z)", conteudo, re.M | re.S
    ):
        numero = int(secao.group(1))
        if numero not in selecionadas:
            continue
        titulo, corpo = secao.group(2), secao.group(3)
        subtitulo = ""
        ignorar_exemplo = False
        contador = 0
        for bloco in re.split(r"\n\s*\n", corpo):
            bloco = bloco.strip()
            if not bloco:
                continue
            if bloco.startswith("**") and bloco.endswith("**"):
                subtitulo = bloco.strip("*")
                ignorar_exemplo = subtitulo.casefold().startswith(
                    ("exemplo", "como testar")
                )
                continue
            if ignorar_exemplo or "```" in bloco:
                continue
            # Linhas de tabela são unidades próprias; cabeçalho é metadado do título.
            linhas = bloco.splitlines()
            if (
                len(linhas) >= 3
                and linhas[0].startswith("|")
                and re.fullmatch(r"\|[\s:|\-]+\|", linhas[1])
            ):
                for linha in linhas[2:]:
                    if linha.strip():
                        contador += 1
                        partes.append(
                            (
                                f"V2026.3-S{numero:02d}-{contador:03d}",
                                titulo
                                + (" — " + subtitulo if subtitulo else "")
                                + " — Colunas: "
                                + linhas[0],
                                linha.strip(),
                                str(numero),
                            )
                        )
                continue
            # Preservar texto contíguo e linhas completas nos demais blocos.
            lote = []
            tamanho = 0
            for linha in bloco.splitlines(keepends=True):
                if lote and tamanho + len(linha) > 1500:
                    contador += 1
                    partes.append(
                        (
                            f"V2026.3-S{numero:02d}-{contador:03d}",
                            titulo + (" — " + subtitulo if subtitulo else ""),
                            "".join(lote).strip(),
                            str(numero),
                        )
                    )
                    lote, tamanho = [], 0
                lote.append(linha)
                tamanho += len(linha)
            if lote:
                contador += 1
                partes.append(
                    (
                        f"V2026.3-S{numero:02d}-{contador:03d}",
                        titulo + (" — " + subtitulo if subtitulo else ""),
                        "".join(lote).strip(),
                        str(numero),
                    )
                )
    if exigir_completude and not selecionadas.issubset({int(p[3]) for p in partes}):
        raise ValueError("Seções operacionais incompletas no manual vigente.")
    return partes


def carregar_trechos(caminho: Path, versao: str) -> list[Trecho]:
    base = carregar_base(caminho, versao)
    compactos = []
    operacionais = []
    resumos = 0
    for documento in base["documentos"]:
        conteudo = documento["texto"]
        partes = []
        if documento.get("anexo_rag"):
            resumos += 1
            bloco = re.search(r"```text\s*\n(.*?)\n```", conteudo, re.S)
            if not bloco:
                raise ValueError("Anexo de recuperação inválido.")
            partes = [
                (m.group(1), m.group(2), m.group(3).strip(), "Anexo B")
                for m in re.finditer(
                    r"\[(RAG-\d+) ([^\]]+)\]\s*\n(.*?)(?=\n\[RAG-|\Z)",
                    bloco.group(1),
                    re.S,
                )
            ]
            compactos.extend(
                Trecho(
                    id_,
                    titulo,
                    texto,
                    documento["fonte"],
                    versao,
                    documento["sha256"],
                    True,
                    obrigatorio=id_ == "RAG-09",
                    secao=secao,
                )
                for id_, titulo, texto, secao in partes
            )
        if documento.get("secoes_indexadas"):
            partes = trechos_secoes_operacionais(conteudo, exigir_completude=False)
            declaradas = set(map(str, documento["secoes_indexadas"]))
            if {p[3] for p in partes} != declaradas:
                raise ValueError("Seções divergem do manifesto.")
            operacionais.extend(
                Trecho(
                    id_,
                    titulo,
                    texto,
                    documento["fonte"],
                    versao,
                    documento["sha256"],
                    True,
                    secao=secao,
                )
                for id_, titulo, texto, secao in partes
            )
    if (
        resumos != 1
        or {t.id for t in compactos} != {f"RAG-{i:02d}" for i in range(1, 10)}
        or len(compactos) != 9
    ):
        raise ValueError("Resumo de recuperação incompleto ou duplicado.")
    if {t.secao for t in operacionais} != {
        "2",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "12",
        "16",
    }:
        raise ValueError("Cobertura operacional incompleta.")
    trechos = compactos + operacionais
    if len({t.id for t in trechos}) != len(trechos):
        raise ValueError("Identificadores duplicados na base.")
    return trechos


class IndiceTFIDF:
    def __init__(self, trechos: list[Trecho]):
        if not trechos or not any(t.obrigatorio for t in trechos):
            raise ValueError("Base sem trechos ou sem privacidade.")
        self.trechos = trechos
        contagens = [Counter(termos(t.titulo + "\n" + t.texto)) for t in trechos]
        frequencias = Counter(t for c in contagens for t in c)
        self.idf = {
            t: math.log((1 + len(trechos)) / (1 + n)) + 1
            for t, n in frequencias.items()
        }
        self.vetores = [self._vetor(c) for c in contagens]

    def _vetor(self, contagem: Counter) -> dict[str, float]:
        pesos = {
            t: (1 + math.log(n)) * self.idf[t]
            for t, n in contagem.items()
            if t in self.idf
        }
        norma = math.sqrt(sum(p * p for p in pesos.values()))
        return {t: p / norma for t, p in pesos.items()} if norma else {}

    def recuperar(self, pergunta: str, limite: int = 3) -> list[Trecho]:
        vetor = self._vetor(Counter(termos(pergunta)))
        pontuados = [
            replace(t, pontuacao=sum(p * v.get(termo, 0) for termo, p in vetor.items()))
            for t, v in zip(self.trechos, self.vetores, strict=True)
        ]
        relevantes = sorted(
            (t for t in pontuados if t.pontuacao > 0),
            key=lambda t: (-t.pontuacao, t.id),
        )[:limite]
        ids = {t.id for t in relevantes}
        return relevantes + [t for t in pontuados if t.obrigatorio and t.id not in ids]
