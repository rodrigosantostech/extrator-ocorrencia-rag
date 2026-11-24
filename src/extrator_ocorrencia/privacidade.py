"""Minimização por padrões; não substitui revisão humana nem garante anonimização."""

import re
import unicodedata


def normalizar(texto: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFKD", texto.casefold())
        if not unicodedata.combining(c)
    )


def mascarar(texto: str, segredos: tuple[str, ...] = ()) -> str:
    for segredo in segredos:
        if segredo:
            texto = texto.replace(segredo, "[SEGREDO_MASCARADO]")
    padroes = (
        (r"\bsk-[A-Za-z0-9_-]+", "[CHAVE_MASCARADA]"),
        (r"(?<!\d)\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}(?!\d)", "[CPF_MASCARADO]"),
        (
            r"(?<!\w)(?:\+?55[\s.-]*)?(?:\(\d{2}\)|\d{2})[\s.-]*9?\d{4}[\s.-]*\d{4}(?!\w)",
            "[TELEFONE_MASCARADO]",
        ),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL_MASCARADO]"),
        (
            r"\b(cliente|paciente)\s+[A-ZÀ-Ý][a-zà-ÿ]+(?:\s+[A-ZÀ-Ý][a-zà-ÿ]+)*",
            r"\1 [NOME_MASCARADO]",
        ),
    )
    for padrao, substituto in padroes:
        texto = re.sub(padrao, substituto, texto)
    return texto


def contem_dado_medico_pessoal(texto: str) -> bool:
    nome_pessoal = re.search(r"\b(?:cliente|paciente)\s+[A-ZÀ-Ý][a-zà-ÿ]+\b", texto)
    texto = normalizar(texto)
    pessoa = nome_pessoal or re.search(
        r"\b(?:cliente|paciente)\s+(?:\w+\s+){0,3}(?:tem|toma|usa|com|diagnosticad[oa])\b|"
        r"\b(?:meu diagnostico|minha receita|tenho diagnostico)\b",
        texto,
    )
    saude = re.search(
        r"\b(receita|diagnostico|doenca|tratamento|hiv|diabetes|cancer|insulina|medicamento)\b",
        texto,
    )
    return bool(pessoa and saude)


def suspeita_injecao(texto: str) -> bool:
    texto = normalizar(texto)
    padroes = (
        r"\bignore\s+(?:todas?\s+)?(?:as\s+)?(?:regras|instrucoes)",
        r"\b(?:mostre|revele|exiba|imprima)\b.{0,60}\b(?:prompt|senha|chave da api|credenciais)\b",
        r"\bsystem\s+override\b",
        r"\bignore\s+(?:all\s+)?(?:previous\s+)?instructions\b",
        r"\b(?:send|reveal|show)\b.{0,45}\b(?:api key|system prompt|password)\b",
        r"</?(?:system|admin|developer)\b",
    )
    return any(re.search(p, texto, re.S) for p in padroes)


def limpar_objeto(objeto: object, segredos: tuple[str, ...] = ()) -> object:
    if isinstance(objeto, str):
        if contem_dado_medico_pessoal(objeto):
            return "[CONTEUDO_PESSOAL_DE_SAUDE_RETIDO]"
        return mascarar(objeto, segredos)
    if isinstance(objeto, dict):
        return {k: limpar_objeto(v, segredos) for k, v in objeto.items()}
    if isinstance(objeto, list):
        return [limpar_objeto(v, segredos) for v in objeto]
    return objeto
