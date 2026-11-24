"""Relatórios locais completos, com escape HTML e auditoria em JSON mascarado."""

import json
import platform
import subprocess
from datetime import datetime, timedelta, timezone
from html import escape
from importlib.metadata import PackageNotFoundError, version
from uuid import uuid4

from .config import Configuracao
from .privacidade import limpar_objeto

CSS = """
:root{color-scheme:light;--ink:#182e45;--muted:#52677b;--line:#d8e3ed;--brand:#176b75}
*{box-sizing:border-box}body{margin:0;background:#f1f5f9;color:var(--ink);font:16px/1.65 system-ui,'Segoe UI',sans-serif;overflow-wrap:anywhere}
header{background:linear-gradient(115deg,#102b45,#176b75);color:#fff;padding:44px max(20px,calc((100vw - 1180px)/2))}
header p{color:#daedf2}h1{font-size:clamp(28px,4vw,44px);letter-spacing:-.035em;line-height:1.15;margin:8px 0}h2{font-size:23px;line-height:1.3;margin:0 0 16px}h3{font-size:18px}
main{max-width:1220px;min-width:0;width:100%;margin:auto;padding:24px 20px}nav{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}a{color:#12546c}nav a{background:white;border:1px solid var(--line);border-radius:8px;padding:9px 14px;text-decoration:none}
a:focus-visible,summary:focus-visible{outline:3px solid #bd7100;outline-offset:4px}section{background:white;border:1px solid var(--line);border-radius:14px;padding:28px;margin-bottom:22px;min-width:0;box-shadow:0 4px 18px #18334b04}
p{margin:8px 0 16px}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:20px 0}.card{border:1px solid var(--line);border-top:3px solid #238a8b;border-radius:10px;padding:18px;background:#f6fafc}.card strong{display:block;font-size:23px;margin-top:8px}.badge{display:inline-block;padding:5px 12px;border-radius:6px;background:#e8f5f0;color:#175b4b;font-weight:700}.warning{border-left:4px solid #bd8625;background:#fff7e5;padding:14px 18px;border-radius:6px;color:#644c18}.muted{color:var(--muted)}
.scroll{overflow-x:auto;max-width:100%;border:1px solid var(--line);border-radius:8px}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:13px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{background:#eef4f8}tbody tr:nth-child(even){background:#f8fafc}caption{text-align:left;font-weight:700;padding:12px}blockquote{margin:12px 0;border-left:3px solid #288b8d;background:#f0f8f8;padding:16px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#102c42;color:#e6eff6;padding:18px;border-radius:8px;font:13px/1.65 Consolas,monospace;max-width:100%}details{border:1px solid var(--line);border-radius:8px;margin:14px 0;padding:14px}summary{cursor:pointer;font-weight:650}footer{padding:20px;text-align:center;color:var(--muted);font-size:13px}
@media(max-width:650px){main{padding:14px 10px}section{padding:18px}.cards{grid-template-columns:1fr}header{padding:28px 16px}.scroll table{min-width:580px}nav a{padding:8px 10px}h2{font-size:21px}}
@media print{body{background:#fff;font-size:10pt}header{background:white;color:#182e45;padding:12px}header p{color:#52677b}main{padding:0}nav{display:none}section{box-shadow:none;border:0;border-top:1px solid #888;border-radius:0;padding:15px 0}pre{background:#eee;color:#111}thead{display:table-header-group}tr,.card{break-inside:avoid}.scroll{overflow:visible}.scroll table{min-width:0}details{break-inside:auto}h2,h3{break-after:avoid}}
"""


AVISO_CONSULTA = (
    "Situação de incidente e gravidade não são atribuídas neste modo de consulta."
)
AVISO_EXTRACAO = (
    "As saídas v1–v3 são comparadas em uma única execução e não substituem a "
    "revisão humana."
)
ESCOPO_CONSULTA = (
    "<p>Os seis campos de extração, associação de mensagens, loja desconhecida, "
    "múltiplas ocorrências, atualizações, conflitos, consolidado por loja e histórico "
    "não são produzidos por este comando. Não há acionamento externo nem alteração "
    "da base.</p><p>Os 16 casos principais e as avaliações complementares de extração, "
    "segurança, privacidade e viés não foram executados por esta consulta. Não há "
    "métricas de qualidade calculadas; ausência de execução não equivale a desempenho "
    "de 0%. Denominadores e julgamento de acertos não se aplicam a uma consulta "
    "isolada.</p>"
)
ESCOPO_EXTRACAO = (
    "<p>Esta execução processa uma única mensagem digitada pelas versões v1, v2 e v3. "
    "Não executa os 16 casos principais, não calcula métricas nem consolida lotes, "
    "associações ou histórico. Não há acionamento externo nem alteração da base.</p>"
    "<p>O manual v2026.3 contém propostas pendentes; por isso a saída v3 sempre exige "
    "revisão humana. A v1 é texto livre sem validação automática.</p>"
)


def _json(objeto: object) -> str:
    return escape(json.dumps(objeto, ensure_ascii=False, indent=2, default=str))


def _estado_versoes(resultado: dict) -> dict[str, str]:
    executadas = {i["versao"]: i["status"] for i in resultado.get("resultados", [])}
    return {v: executadas.get(v, "NÃO EXECUTADO") for v in ("v1", "v2", "v3")}


def _html_versoes_extracao(resultados: list[dict]) -> str:
    linhas = ""
    for item in resultados:
        saida = item.get("saida") or item.get("resposta_bruta") or item.get("motivo")
        if isinstance(saida, dict):
            saida = json.dumps(saida, ensure_ascii=False, indent=2)
        erros = item.get("validacoes", {}).get("erros", [])
        linhas += (
            "<tr><th>"
            + escape(item["versao"])
            + "</th><td>"
            + escape(item["prompt_id"])
            + "</td><td>"
            + escape(item["status"])
            + "</td><td><pre>"
            + escape(str(saida or "Sem saída."))
            + "</pre></td><td>"
            + escape(", ".join(erros) or "—")
            + "</td></tr>"
        )
    return (
        '<section id="versoes"><h2>Comparação de extração v1, v2 e v3</h2><p>A mesma '
        "mensagem foi processada pelas três versões em uma única execução; o resultado "
        'não é o benchmark de 16 casos.</p><div class="scroll"><table><caption>'
        "Resultado por versão</caption><thead><tr><th>Versão</th><th>Prompt</th>"
        "<th>Estado</th><th>Saída</th><th>Erros de validação</th></tr></thead><tbody>"
        + linhas
        + "</tbody></table></div></section>"
    )


def _codigo(raiz) -> dict[str, object]:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=raiz, text=True, stderr=subprocess.DEVNULL
        ).strip()
        sujo = bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=raiz,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        )
        return {"commit": sha, "alteracoes_locais": sujo}
    except (OSError, subprocess.SubprocessError):
        return {"commit": "INDISPONÍVEL", "alteracoes_locais": "INDISPONÍVEL"}


def salvar_relatorio(
    cfg: Configuracao, resultado: dict, comando: str
) -> tuple[dict[str, object], object, object]:
    agora = datetime.now(timezone(timedelta(hours=-3)))
    id_ = agora.strftime("execucao_%Y%m%d_%H%M%S_") + uuid4().hex[:8]
    try:
        sdk = version("openai")
    except PackageNotFoundError:
        sdk = "NÃO INSTALADO"
    extracao = resultado.get("modo") == "comparacao_prompts"
    titulo = (
        "Extração e comparação de prompts"
        if extracao
        else "Consulta fundamentada no manual"
    )
    chamadas = resultado.get("chamadas", [])
    total_chamadas = sum(bool(c.get("tentativa_http")) for c in chamadas)
    custos = [c.get("custo_usd_estimado") for c in chamadas if c.get("tentativa_http")]
    registro = limpar_objeto(
        {
            "contrato_versao": "extracao-prompts-1" if extracao else "consulta-rag-1",
            "execucao": id_,
            "data_hora": agora.isoformat(),
            "fuso": "America/Sao_Paulo (UTC-03:00)",
            "comando": comando,
            "codigo": _codigo(cfg.raiz),
            "python": platform.python_version(),
            "sdk_openai": sdk,
            "modelo": cfg.modelo,
            "parametros": cfg.parametros,
            "timeout_segundos": cfg.timeout_segundos,
            "repeticoes_automaticas": 0,
            "dataset": "ENTRADA ÚNICA DIGITADA" if extracao else "NÃO UTILIZADO",
            "congelamento": "NÃO APLICÁVEL À CONSULTA",
            "comparacao_extracao": _estado_versoes(resultado),
            "chamadas_http_tentadas": total_chamadas,
            "custo_usd_estimado": sum(custos)
            if custos and all(c is not None for c in custos)
            else None,
            "resultado": resultado,
        },
        (cfg.chave_api,),
    )
    # Retenção conservadora de qualquer campo que ainda pareça conter dados pessoais de saúde.
    cfg.resultados.mkdir(parents=True, exist_ok=True)
    html_path = cfg.resultados / (id_ + ".html")
    json_path = cfg.resultados / (id_ + ".json")
    json_path.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    r = registro["resultado"]
    status = escape(str(r.get("status", "INDISPONÍVEL")))
    pergunta = escape(str(r.get("entrada", "Não se aplica a este comando.")))
    resposta = escape(
        str(
            r.get(
                "resposta",
                r.get(
                    "motivo",
                    "Veja a comparação por versão abaixo."
                    if extracao
                    else "Consulte os dados completos abaixo.",
                ),
            )
        )
    )
    html = (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'
        + titulo
        + " · Rede Saúde Viva</title><style>"
        + CSS
        + "</style></head><body>"
    )
    html += (
        "<header><p>REDE SAÚDE VIVA · PROTÓTIPO ACADÊMICO</p><h1>"
        + escape(titulo)
        + "</h1><p>"
        + escape(id_)
        + " · "
        + escape(agora.isoformat())
        + " · America/Sao_Paulo</p></header><main>"
    )
    html += '<nav aria-label="Seções do relatório"><a href="#resultado">Resultado</a><a href="#fontes">Fontes recuperadas</a><a href="#versoes">v1–v3</a><a href="#auditoria">Auditoria</a><a href="#limites">Limitações</a></nav>'
    html += (
        '<section id="resultado"><h2>Resultado da execução</h2><div class="cards"><div class="card">Estado técnico<strong>'
        + status
        + '</strong></div><div class="card">Modelo configurado<strong>'
        + escape(str(registro["modelo"]))
        + '</strong></div><div class="card">Chamadas HTTP tentadas<strong>'
        + str(total_chamadas)
        + '</strong></div></div><p class="warning">Revisão humana: '
        + (
            "necessária"
            if r.get("requer_revisao_humana", True)
            else "não exigida pelos controles automáticos; continua disponível"
        )
        + ". "
        + (AVISO_EXTRACAO if extracao else AVISO_CONSULTA)
        + "</p><h3>Entrada utilizada, com minimização</h3><p>"
        + pergunta
        + '</p><h3>Resposta</h3><p style="white-space:pre-wrap">'
        + resposta
        + "</p>"
    )
    for citacao in r.get("citacoes", []):
        html += (
            "<blockquote><strong>"
            + escape(citacao["trecho_id"])
            + "</strong><br>"
            + escape(citacao["citacao"])
            + "</blockquote>"
        )
    html += (
        "<h3>Validações e alertas</h3><pre>"
        + _json(
            {"validacoes": r.get("validacoes", {}), "alertas": r.get("alertas", [])}
        )
        + "</pre></section>"
    )
    html += '<section id="fontes"><h2>Trechos efetivamente recuperados</h2><p>Até três resultados de pontuação positiva, mais privacidade obrigatória. Pontuação é similaridade lexical por cosseno, sem interpretação de confiança ou probabilidade.</p>'
    trechos = r.get("trechos_recuperados", [])
    if not trechos:
        html += "<p>Nenhum trecho recuperado ou disponibilizado nesta execução.</p>"
    for t in trechos:
        html += (
            "<details open><summary>"
            + escape(t["id"])
            + " · "
            + escape(t["titulo"])
            + " · cosseno "
            + f"{t['pontuacao']:.5f}"
            + '</summary><p class="muted">Fonte: '
            + escape(t["fonte"])
            + " · versão "
            + escape(t["versao"])
            + " · obrigatório: "
            + ("sim" if t["obrigatorio"] else "não")
            + " · propostas pendentes: "
            + ("sim" if t["proposta_pendente"] else "não")
            + "</p><pre>"
            + escape(t["texto"])
            + "</pre><p>SHA-256: "
            + escape(t["sha256"])
            + "</p></details>"
        )
    html += "</section>"
    html += (
        _html_versoes_extracao(r["resultados"])
        if extracao
        else '<section id="versoes"><h2>Comparação de extração v1, v2 e v3</h2><p>Este é o assistente de consulta RAG, com contrato próprio. Não representa execução do benchmark de extração.</p><div class="scroll"><table><caption>Estado explícito das versões do benchmark</caption><thead><tr><th>Aspecto</th><th>v1</th><th>v2</th><th>v3</th></tr></thead><tbody><tr><th>Técnicas planejadas</th><td>Zero-shot e saída livre</td><td>Persona, few-shot e JSON</td><td>Filtro e extração com RAG</td></tr><tr><th>Execução nesta consulta</th><td>Não executado</td><td>Não executado</td><td>Não executado</td></tr><tr><th>Entradas, saídas, acertos, falhas, regressões e custos por versão</th><td>Indisponíveis</td><td>Indisponíveis</td><td>Indisponíveis</td></tr></tbody></table></div></section>'
    )
    html += (
        '<section id="auditoria"><h2>Configuração e auditoria completa</h2><p>Inclui entrada mascarada, versões dos prompts, contexto, respostas brutas mascaradas, resposta estruturada, falhas tratadas, latência e tokens por chamada, quando disponíveis. JSON complementar: '
        + escape(json_path.name)
        + ".</p><details><summary>Exibir todos os dados desta execução</summary><pre>"
        + _json(registro)
        + "</pre></details></section>"
    )
    html += (
        '<section id="limites"><h2>Limitações e itens não executados</h2><p>Somente dados fictícios ou sintéticos. Mascaramento e filtros reduzem riscos, mas não garantem proteção absoluta. A validação de citação literal não comprova que todas as afirmações são sustentadas; exige avaliação humana.</p>'
        + (ESCOPO_EXTRACAO if extracao else ESCOPO_CONSULTA)
        + "<p>Custos, quando presentes, são estimativas pelo preço publicado em 23/11/2026: (entrada × US$ 0,10 + saída × US$ 0,50) / 1.000.000 para gpt-6-luna, sem descontos de cache. Outros modelos ficam sem estimativa. Não é fatura nem confirmação de saldo. Versões não congeladas e alterações locais são identificadas na auditoria.</p></section></main><footer>Relatório local em UTF-8 · conteúdo externo escapado · sem recursos de terceiros</footer></body></html>"
    )
    html_path.write_text(html, encoding="utf-8")
    return registro, html_path, json_path
