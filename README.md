# Extrator de Ocorrências com RAG

Projeto acadêmico de extração e triagem de mensagens operacionais da empresa fictícia **Rede Saúde Viva**, com comparação de prompts v1, v2 e v3, consulta ao manual operacional e avaliação de segurança.

A implementação planejada usa **Python local no Windows e GPT pela API da OpenAI**.

## Documentação

- [Requisitos oficiais do MBA](docs/TRABALHO_MBA.md): consolidação das exigências R1–R5 e dos entregáveis E1–E4.

- [Referência aproximada da solução pretendida](docs/Trabalho_Final_MBA_Extrator_Ocorrencias.md): guia do que queremos construir, com problema, prompts, manual, 16 casos e ideias para relatório e pitch. Os detalhes serão adaptados às decisões do projeto e às exigências do professor.
- [Passo a passo de execução](docs/PASSO_A_PASSO.md): tarefas, dependências, critérios de conclusão e cronograma adaptados às decisões do projeto.

## Objetivo operacional confirmado

**21/11/2026 — origem: esclarecimento do usuário nesta conversa.** Apoiar a área que acompanha ocorrências em lojas, como assaltos e outros incidentes, recebidas em mensagens textuais pelo WhatsApp. Processar o conjunto de mensagens e consolidar ocorrências por loja e prioridade, relacionando relatos e atualizações com fontes rastreáveis.

Fluxo planejado: lote de mensagens → mascaramento e triagem → extração e consulta ao manual → validação → associação de relatos e atualizações → consolidado → revisão humana.

O RAG fornece as regras de classificação e ação. A consolidação relaciona as mensagens e preserva ocorrências distintas. O protótipo deve validar lotes sintéticos por arquivo; a conexão automática ao WhatsApp permanece uma evolução proposta, sem conector implementado ou definido. Áudios e imagens ficam fora do recorte textual.

## Base de conhecimento

- [Manual de operações da Rede Saúde Viva](data/documents/manual_operacoes_saude_viva.md): primeiro documento da base, versão 2026.1, com cadastro de lojas, classificação de ocorrências e privacidade. Convertido do arquivo fornecido pelo usuário, preservando o conteúdo operacional.
- [Manual de operações v2026.3](data/documents/manual_operacoes_saude_viva_v2026.3.md): adequação da v2026.2 elaborada pelo usuário, com regras do v2026.1 marcadas e regras novas identificadas como propostas a validar, incluindo consultas de preço, procura de produtos, segurança patrimonial, consolidação e trechos identificados para recuperação. Versão em Word em [docs/anexos/](docs/anexos/).

## Casos complementares

[data/datasets/complementares/](data/datasets/complementares/) reúne 71 casos sintéticos (IDs 17 a 87), separados do benchmark principal de 16 casos, a exportação textual do grupo de WhatsApp gerada a partir deles e o gabarito da consolidação do lote. Os casos ainda não foram executados em nenhuma versão de prompt.

## Estado atual

A documentação, o primeiro manual e a estrutura inicial do pacote Python foram preparados. Há configuração de caminhos, diagnóstico local do manual e testes sem API. Extração v1–v3, recuperação RAG, consolidação, dataset executável e benchmark continuam pendentes. A configuração da chave foi adiada por solicitação do usuário em 21/11/2026.

Conforme esclarecimento do usuário em 21/11/2026, o documento convertido representa, em linhas gerais, o que queremos fazer; orienta a solução sem fixar todos os detalhes. Suas referências a Gemini/Colab ficam como histórico, pois a implementação planejada usa Python no Windows e API da OpenAI. Percentuais, proteções e status declarados no Word continuam sem comprovação neste repositório.

## Próximas entregas

1. Revisar os requisitos e as divergências entre manual e casos esperados.
2. Preparar Python, acesso à API e os 16 casos de teste.
3. Implementar e comparar v1/v2 para o checkpoint de **23/11/2026**.
4. Implementar recuperação, v3, validações, consolidação em lote e avaliações separadas de extração e consolidação.
5. Finalizar relatório de até oito páginas e pitch de sete minutos para **25/11/2026**.

## Preparação e comandos locais

Execute na raiz do repositório, no Windows PowerShell, com Python 3.12 instalado. Após a instalação do Python, reabra o terminal para atualizar os comandos disponíveis:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m extrator_ocorrencia diagnostico
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os comandos usam diretamente o ambiente virtual e dispensam sua ativação. Para consultar o manual a partir de outro diretório, informe `diagnostico --raiz C:\Dev\extrator-ocorrencia-rag`. O diagnóstico retorna código 0 quando o manual é legível, está em UTF-8 e não está vazio; retorna 1 em caso de falha. Isso verifica a leitura do arquivo, sem validar suas regras nem implementar recuperação.

A base atual usa somente a biblioteca padrão. O `pip` pode acessar a rede para obter a ferramenta de empacotamento `setuptools`. SDK da OpenAI, validação estruturada e recuperação lexical serão acrescentados nas etapas correspondentes; suas versões serão fixadas após validação. O arquivo `.env.example` está reservado para configuração futura; o código atual não carrega arquivos `.env`.

## Organização inicial

| Caminho | Finalidade |
| --- | --- |
| `pyproject.toml` | Metadados do pacote, requisito de Python e comando `extrator-ocorrencias` |
| `src/extrator_ocorrencia/config.py` | Caminhos locais centralizados |
| `src/extrator_ocorrencia/cli.py` | Diagnóstico do manual, sem API |
| `tests/` | Testes locais com `unittest` |
| `data/documents/` | Base documental existente |
| `data/datasets/` | Casos de avaliação; contém apenas os casos complementares em `complementares/` |
| `docs/anexos/` | Versão em Word do manual v2026.3 |
| `data/examples/` | Espaço reservado a exemplos sintéticos de desenvolvimento; ainda vazio |
| `results/` | Resultados locais futuros, ignorados pelo Git |

As pastas `data/examples/` e `results/` contêm apenas `.gitkeep`. Os casos complementares estão preparados, mas os 16 casos do benchmark principal ainda não foram criados nem congelados. Resultados selecionados para entrega deverão ser exportados e versionados explicitamente, após revisão de privacidade; a pasta local ignorada não constitui evidência entregue.
