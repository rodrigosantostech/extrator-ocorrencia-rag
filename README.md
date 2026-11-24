# Extrator de Ocorrências com RAG

Projeto acadêmico de extração e triagem de mensagens operacionais da empresa fictícia **Rede Saúde Viva**, com comparação de prompts v1, v2 e v3, consulta ao manual operacional e avaliação de segurança.

O protótipo usa **Python local no Windows e a API da OpenAI**. Hoje oferece dois modos: **extrair uma ocorrência de uma mensagem**, comparando v1, v2 e v3, e **consultar o manual operacional com fontes citadas**. As execuções tentam gerar relatório HTML e registro JSON locais; os limites de geração estão descritos abaixo.

O público-alvo é a área de operações que acompanha incidentes em lojas. Este README explica a finalidade, as técnicas e os passos para instalar, executar e conferir o protótipo. Use somente dados fictícios ou sintéticos.

## Documentação

- [Requisitos oficiais do MBA](docs/TRABALHO_MBA.md): consolidação das exigências R1–R5 e dos entregáveis E1–E4.

- [Referência aproximada da solução pretendida](docs/Trabalho_Final_MBA_Extrator_Ocorrencias.md): guia do que queremos construir, com problema, prompts, manual, 16 casos e ideias para relatório e pitch. Os detalhes serão adaptados às decisões do projeto e às exigências do professor.
- [Passo a passo de execução](docs/PASSO_A_PASSO.md): tarefas, dependências, critérios de conclusão e cronograma adaptados às decisões do projeto.

## Objetivo operacional confirmado

**21/11/2026 — origem: esclarecimento do usuário nesta conversa.** Apoiar a área que acompanha ocorrências em lojas, como assaltos e outros incidentes, recebidas em mensagens textuais pelo WhatsApp. Processar o conjunto de mensagens e consolidar ocorrências por loja e prioridade, relacionando relatos e atualizações com fontes rastreáveis.

Fluxo planejado: lote de mensagens → mascaramento e triagem → extração e consulta ao manual → validação → associação de relatos e atualizações → consolidado → revisão humana.

O RAG fornece as regras de classificação e ação. A consolidação relaciona as mensagens e preserva ocorrências distintas. O protótipo deve validar lotes sintéticos por arquivo; a conexão automática ao WhatsApp permanece uma evolução proposta, sem conector implementado ou definido. Áudios e imagens ficam fora do recorte textual.

## Por que criar este assistente com RAG?

Relatos operacionais chegam em mensagens informais, com abreviações, erros de digitação e informações incompletas. A área de operações precisa identificar a loja, entender o ocorrido, consultar a regra aplicável e decidir o que deve receber atenção primeiro. Fazer essa leitura e cruzar cada relato com o manual é a tarefa que o protótipo pretende apoiar; a redução de tempo e de erros ainda precisa ser medida.

A IA generativa é usada para interpretar o texto e produzir uma descrição estruturada. A hipótese é que ela consiga lidar com variações de linguagem sem exigir uma regra fixa para cada forma de escrever. Regras determinísticas continuam úteis para limites de entrada, mascaramento, validação de formato e conferência de citações.

**RAG (geração aumentada por recuperação)** conecta essa interpretação às regras documentadas da Rede Saúde Viva. Antes de responder, o sistema busca trechos relevantes do manual e os fornece ao modelo como contexto. Isso permite:

- **Fundamentar a orientação:** classificação e ação devem se apoiar nas regras recuperadas, com citação literal no v3.
- **Rastrear a fonte:** cada trecho registra ID, documento, versão, hash e pontuação de recuperação.
- **Manter o conhecimento separado do modelo:** as regras podem ser revisadas nos documentos e no manifesto, sem treinar novamente o modelo.
- **Explicitar limites:** evidência insuficiente, propostas pendentes e falhas de validação precisam aparecer para revisão humana.

O RAG foi escolhido porque a informação específica está em um manual versionado. O ajuste fino de parâmetros (*fine-tuning*) pode ser útil para aprender padrões de tarefa ou estilo, mas não é necessário para disponibilizar essas regras na consulta. A multimodalidade fica fora do recorte atual, que recebe apenas texto. A recuperação não garante que o trecho encontrado seja suficiente nem que a interpretação esteja correta.

## Técnicas utilizadas

| Técnica | Aplicação no código atual | Finalidade |
| --- | --- | --- |
| Zero-shot | v1 recebe uma instrução curta, sem exemplos e com resposta livre | Preservar uma referência inicial de comparação |
| Persona e few-shot | v2 define o papel de assistente operacional e apresenta um exemplo de entrada e JSON | Orientar a tarefa e demonstrar o formato esperado |
| JSON Schema estrito | v2, v3 e etapas estruturadas de consulta e segurança | Restringir campos e tipos; validação local complementa o formato |
| Encadeamento de prompts | v3 faz filtro de segurança e depois extração; `consultar` faz filtro e depois resposta | Separar a análise de segurança da geração, quando o fluxo prossegue |
| RAG lexical | TF-IDF e similaridade de cosseno sobre o manual v2026.3 | Recuperar até três trechos com pontuação positiva, mais privacidade obrigatória |
| Validação e minimização | Mascaramento por padrões, filtros locais, validação de campos e citações | Reduzir exposição de dados e reter respostas inconsistentes para revisão |

A recuperação é implementada com a biblioteca padrão do Python, adequada ao tamanho atual da base. Normaliza caixa, acentos e formas de loja para a busca, preservando o texto original das citações. Não utiliza serviço externo de embeddings nem banco vetorial.

| Versão de extração | Contexto e formato | Hipótese a avaliar |
| --- | --- | --- |
| v1 | Mensagem mascarada, zero-shot, sem RAG e com saída livre preservada | Estabelecer a referência inicial |
| v2 | Mesma mensagem, persona, few-shot e cinco campos em JSON, sem RAG | Melhorar a organização e a consistência do formato |
| v3 | Mesma mensagem, filtro de segurança, trechos RAG e seis campos em JSON, incluindo `regra_consultada` | Melhorar a fundamentação e permitir conferência da fonte |

As versões usam o mesmo modelo e os parâmetros centralizados da execução. A comparação envolve tanto mudanças nos prompts quanto a restrição de saída da API em v2/v3. O benchmark ainda não foi executado; essas hipóteses não são resultados medidos. Em `extrair`, v1 e v2 são executadas antes do filtro específico do v3; esse filtro não protege retroativamente as outras versões.

## Base de conhecimento

A base vigente é o **manual v2026.3 dividido por assunto**, em [data/documents/manual_v2026_3/](data/documents/manual_v2026_3/). O [manifesto](data/documents/manual_v2026_3/manifesto.json) define arquivos, hashes, ordem original e conteúdo permitido na recuperação.

| Arquivo | Assunto |
| --- | --- |
| [00_contexto.md](data/documents/manual_v2026_3/00_contexto.md) | Identificação, origem e escopo |
| [01_lojas.md](data/documents/manual_v2026_3/01_lojas.md) | Diretório e resolução de lojas |
| [02_fluxo_e_contrato.md](data/documents/manual_v2026_3/02_fluxo_e_contrato.md) | Fluxo e campos de extração |
| [03_gravidade_e_decisao.md](data/documents/manual_v2026_3/03_gravidade_e_decisao.md) | Gravidade, ações, limites e desempate |
| [04_taxonomia.md](data/documents/manual_v2026_3/04_taxonomia.md) | Catálogo de ocorrências |
| [05_prioridade.md](data/documents/manual_v2026_3/05_prioridade.md) | Pontuação e ordem da fila |
| [06_linguagem_e_equidade.md](data/documents/manual_v2026_3/06_linguagem_e_equidade.md) | Linguagem informal e equidade |
| [07_seguranca_e_privacidade.md](data/documents/manual_v2026_3/07_seguranca_e_privacidade.md) | Segurança e privacidade |
| [08_avaliacao_e_historico.md](data/documents/manual_v2026_3/08_avaliacao_e_historico.md) | Avaliação, rastreabilidade e decisões |
| [09_consolidacao.md](data/documents/manual_v2026_3/09_consolidacao.md) | Associação, atualizações e consolidado |
| [10_exemplos.md](data/documents/manual_v2026_3/10_exemplos.md) | Exemplos sintéticos; fora do índice |
| [11_resumo_rag.md](data/documents/manual_v2026_3/11_resumo_rag.md) | Nove blocos compactos, com privacidade obrigatória |

Cada documento identifica versão, data, origem e uso; o corpo original foi preservado literalmente. O [manual v2026.3 integral](docs/referencias/manual_operacoes_saude_viva_v2026.3.md) foi arquivado para auditoria e fica fora do índice. O antigo `manual_operacoes_saude_viva.md`, v2026.1, foi removido por solicitação do usuário. A versão em Word é mencionada no histórico do projeto, mas a pasta `docs/anexos/` não está disponível nesta cópia do repositório.

A divisão facilita manutenção e identificação das fontes. Ela preservou os 189 trechos e, nas seis perguntas de conferência, os mesmos IDs e pontuações; não foi medida melhoria de qualidade pela divisão física. Marcações de proposta e conteúdo sintético permanecem identificados.

## Casos complementares

[data/datasets/complementares/](data/datasets/complementares/) reúne 71 casos sintéticos (IDs 17 a 87), separados do benchmark principal de 16 casos, a exportação textual do grupo de WhatsApp gerada a partir deles e o gabarito da consolidação do lote. Os casos ainda não foram executados em nenhuma versão de prompt.

## Estado atual

O assistente de consulta RAG está implementado: recupera trechos do manual por TF-IDF, consulta a Responses API da OpenAI com filtro de segurança e valida citações literais. Usa `gpt-6-luna` por padrão e gera relatório HTML e registro JSON locais. Duas consultas sintéticas reais foram conferidas em 23/11/2026; 35 testes locais sem API passaram após a migração, incluindo seis perguntas sintéticas de cobertura da recuperação e validação do manifesto. A extração de ocorrências v1–v3 está disponível como execução única de uma mensagem (comando `extrair` e executável); a consolidação em lote e o benchmark principal continuam pendentes. Esses testes não comprovam as metas acadêmicas de extração.

Conforme esclarecimento do usuário em 21/11/2026, o documento convertido representa, em linhas gerais, o que queremos fazer; orienta a solução sem fixar todos os detalhes. Suas referências a Gemini/Colab ficam como histórico, pois a implementação planejada usa Python no Windows e API da OpenAI. Percentuais, proteções e status declarados no Word continuam sem comprovação neste repositório.

## Próximas entregas

1. Revisar divergências entre manual e expectativas, preparar e congelar os 16 casos principais.
2. Completar a validação operacional de loja, gravidade e ação; executar os mesmos casos em v1, v2 e v3 e calcular métricas com numeradores e denominadores.
3. Implementar e avaliar a associação de relatos, atualizações e consolidação em lote, preservando ocorrências secundárias.
4. Finalizar relatório de até oito páginas e pitch de sete minutos para **25/11/2026**, com evidências e limitações.

## Preparação e comandos locais

Pré-requisitos: Windows, Python 3.12 e acesso à internet para instalar dependências. A consulta completa e a extração exigem uma chave da API da OpenAI com acesso ao modelo configurado; podem gerar cobrança. O diagnóstico e a recuperação local funcionam sem chave.

### 1. Preparar o ambiente

Abra o Windows PowerShell na raiz do repositório. Após instalar o Python, reabra o terminal para atualizar os comandos disponíveis:

```powershell
Set-Location C:\Dev\extrator-ocorrencia-rag
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m extrator_ocorrencia diagnostico
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\ruff.exe check src tests
.\.venv\Scripts\ruff.exe format --check src tests
```

Os comandos usam diretamente o ambiente virtual e dispensam sua ativação. A opção `[dev]` instala o Ruff, usado para verificar estilo e formatação conforme a configuração do projeto; `ruff format --check` apenas verifica e não altera arquivos. Para consultar o manual a partir de outro diretório, informe `diagnostico --raiz C:\Dev\extrator-ocorrencia-rag`. O diagnóstico retorna código 0 quando a base pode ser lida e confere com o manifesto; retorna 1 em caso de falha. Verifica integridade documental, sem chamar a API, gerar respostas ou validar a correção operacional das regras.

O manifesto inclui o SDK oficial `openai==3.58.0`, validado com Python 3.12.10. O `pip` pode acessar a rede para instalar as dependências e `setuptools`. Nos comandos `consultar` e `extrair`, a configuração lê `OPENAI_API_KEY` e, opcionalmente, `OPENAI_MODEL` do `.env` local ignorado pelo Git; variáveis do processo têm precedência. Preserve a chave fora da conversa e do repositório. O modelo padrão validado é `gpt-6-luna`, com raciocínio desativado, limite de 900 tokens de saída por chamada, tempo limite de 30 segundos e nenhuma repetição automática. Outros modelos configurados precisam suportar esses parâmetros e JSON Schema; não há troca automática de modelo.

### 2. Conferir a recuperação sem usar a API

```powershell
.\.venv\Scripts\python.exe -m extrator_ocorrencia consultar "Qual ação para assalto à mão armada?" --somente-recuperar
```

Confira `trechos_recuperados`, IDs, fontes e pontuações no resultado. O estado `RECUPERADO` indica que houve recuperação local; não significa que o modelo respondeu. O terminal informa os caminhos do HTML e do JSON em `results\`.

### 3. Configurar o acesso à API

Se ainda não houver um `.env`, copie `.env.example` para `.env` na raiz do projeto. Edite somente a cópia local e preencha `OPENAI_API_KEY` com sua chave. Preserve o `.env` existente se já estiver configurado. `OPENAI_MODEL` é opcional; o padrão do código é `gpt-6-luna`. Uma variável do processo tem precedência sobre o arquivo.

O `.env` é ignorado pelo Git. Não inclua a chave nas mensagens de teste, nos comandos de extração ou nos arquivos de documentação.

### 4. Extrair uma mensagem e comparar v1, v2 e v3

Exemplo de entrada sintética, sem resultado previamente medido:

```powershell
.\.venv\Scripts\python.exe -m extrator_ocorrencia extrair "Loja 02 Jardins: sistema PDV parado há 3 horas em horário comercial."
```

O comando processa **uma mensagem** e executa v1, v2 e v3, com até quatro chamadas à API quando todas as etapas prosseguem. Bloqueios e falhas podem interromper etapas. Para ler a mensagem de um arquivo UTF-8 já existente:

```powershell
.\.venv\Scripts\python.exe -m extrator_ocorrencia extrair --arquivo .\mensagem.txt
```

Informe texto entre aspas **ou** `--arquivo`. O limite é de 6.000 caracteres e, para arquivo, 24.000 bytes; o arquivo não representa um lote de mensagens.

Quando há extração estruturada, v2 produz `loja`, `tipo_ocorrencia`, `gravidade`, `acao_necessaria` e `responsavel_contato`; v3 acrescenta `regra_consultada`. A saída livre de v1 permanece disponível. Ausências em loja e responsável usam `null` no v2 e `NÃO INFORMADO` no v3. O schema do v3 também admite `NÃO INFORMADO` para gravidade sem evidência; isso indica uma lacuna para revisão, não um quinto nível de gravidade.

### 5. Consultar o manual

Para fazer uma pergunta sobre as regras, em vez de extrair uma ocorrência:

```powershell
.\.venv\Scripts\python.exe -m extrator_ocorrencia consultar "Qual é a ação e o prazo para um assalto à mão armada na loja?"
```

O comando pode realizar até duas chamadas: filtro de segurança e resposta fundamentada. O contrato da consulta contém resposta e citações; ele é diferente do contrato de extração. Veja as opções e os estados nas seções abaixo.

### 6. Abrir o resultado e conferir as pendências

O terminal retorna `relatorio_html` e `registro_json`. Abra o caminho indicado em `relatorio_html` no navegador. Em execuções pelo Python, os arquivos ficam em `results\` na raiz usada pelo comando.

No HTML de extração, confira a entrada comum, as respostas v1–v3, os trechos recuperados, as validações e os motivos de revisão. No JSON, confira a configuração, as chamadas, as respostas brutas mascaradas, a latência e o uso de tokens quando disponíveis. `EXECUTADO` indica execução, sem certificar acerto operacional; `REVISAO_NECESSARIA`, `BLOQUEADO` e `ERRO_TECNICO` precisam ser interpretados separadamente.

A v2026.3 contém propostas pendentes: as respostas baseadas nela exigem revisão humana. A validação atual da extração confere campos, tipos, valores permitidos de gravidade e literalidade da citação no v3; a validação operacional completa de loja, gravidade e ação permanece pendente. Não há acionamento automático de pessoas ou sistemas externos. Relatórios de execução são locais e não devem ser versionados.

### Executável Windows (alternativa ao Python)

Depois de instalar as dependências de desenvolvimento, gere o executável autônomo:

```powershell
.\scripts\build_exe.cmd
.\dist\ExtratorOcorrencias.exe
```

O executável faz uma única pergunta (`Digite o prompt:`), executa o processo completo sobre o texto informado — mascaramento, filtro de segurança, recuperação no manual e extração pelos prompts v1, v2 e v3 —, gera o relatório HTML/JSON em `results\` ao lado do `.exe`, abre o HTML e encerra. A janela só aguarda ENTER quando há falha, para que a mensagem possa ser lida. A chave não é solicitada nem incluída no executável: configure `OPENAI_API_KEY` no ambiente ou em um arquivo `.env` ao lado do `.exe`. O manual modular v2026.3 é incluído no pacote.

O mesmo fluxo está disponível sem interação: `.\dist\ExtratorOcorrencias.exe extrair "mensagem sintética"` (também aceita `--arquivo`, `--modelo`, `--max-output-tokens` e `--timeout-segundos`).

**Limite atual:** a execução processa uma única mensagem. A avaliação do benchmark principal de 16 casos, o cálculo de métricas e a consolidação de lotes continuam pendentes.

### Consultar o manual

Use somente perguntas fictícias ou sintéticas. A entrada é uma pergunta de até 6.000 caracteres, por argumento ou arquivo UTF-8 de até 24.000 bytes. O arquivo contém uma única consulta; não é um lote do WhatsApp.

```powershell
# Recuperação local: não exige chave nem realiza chamadas à API.
.\.venv\Scripts\python.exe -m extrator_ocorrencia consultar "Qual ação para assalto à mão armada?" --somente-recuperar

# Consulta completa: filtro de segurança e resposta fundamentada, até duas chamadas.
.\.venv\Scripts\python.exe -m extrator_ocorrencia consultar "Qual é a ação e o prazo para um assalto à mão armada na loja?"

# Base vigente v2026.3 (também usada quando --manual é omitido).
.\.venv\Scripts\python.exe -m extrator_ocorrencia consultar "O manual permite informar preço e estoque de produtos?" --manual 2026.3

# Alternativa à pergunta por argumento; consulta.txt deve existir.
.\.venv\Scripts\python.exe -m extrator_ocorrencia consultar --arquivo .\consulta.txt
```

`--raiz` também está disponível em `consultar`. Consulta e diagnóstico carregam `data/documents/manual_v2026_3/manifesto.json`; `--manual 2026.3` é opcional e é a única versão disponível na CLI. O índice conserva 189 trechos: os nove blocos do Anexo B mais conteúdo literal das seções 2, 4, 5, 6, 7, 8, 9, 12 e 16. Tabelas são divididas por linha, com cabeçalho no título; títulos e textos participam da busca. Cada trecho registra seu arquivo de origem, seção, versão e hash. O hash da base identifica o manifesto, que lista os hashes de todos os documentos; o hash do original também aparece no diagnóstico. Exemplos calculados, saídas do Anexo A, gabaritos e a referência integral arquivada ficam fora do índice. Arquivo ausente, conteúdo alterado sem atualização do manifesto ou caminho fora da base causam falha explícita. As propostas e a revisão humana do protótipo permanecem preservadas.
Ao revisar um documento, preserve as marcações e o corpo original entre os delimitadores de conteúdo. Registre a justificativa no passo a passo, revise a mudança e atualize seu `sha256` no manifesto; o valor pode ser obtido com `Get-FileHash -Algorithm SHA256 -LiteralPath <arquivo>`. Não remova a conferência de hash para aceitar uma alteração. Execute os testes e o diagnóstico após a revisão. Não há ganho de autoridade ou aprovação operacional por editar o manifesto.

A recuperação usa TF-IDF com frequência logarítmica, IDF suavizado e similaridade de cosseno, implementados na biblioteca padrão para esta base pequena. Normaliza caixa, acentos e formas de loja para a busca; não altera o texto citado. Seleciona até três resultados com pontuação positiva e acrescenta privacidade obrigatória, sem enviar o manual inteiro. Correspondência lexical não comprova suficiência nem confiança na resposta.

### Entrada, saída e auditoria da consulta

A saída no terminal contém `status`, `resultado`, `relatorio_html` e `registro_json`. O contrato `consulta-rag-1` é próprio do assistente de consulta e não substitui os seis campos planejados para a extração de ocorrências.

| Campo de `resultado` | Conteúdo |
| --- | --- |
| `entrada` | Pergunta utilizada, com minimização de dados |
| `status` | `RESPONDIDO`, `REVISAO_NECESSARIA`, `SEM_EVIDENCIA`, `BLOQUEADO`, `ERRO_TECNICO` ou `RECUPERADO` no modo local |
| `resposta` | Resposta fundamentada ou motivo de retenção, bloqueio ou falha |
| `citacoes` | Lista de `trecho_id` e `citacao` literal, conferidos contra os trechos recuperados |
| `requer_revisao_humana` | Separado do estado técnico; obrigatório para fontes v2026.3 e orientação crítica |
| `trechos_recuperados` | IDs, texto, pontuação, fonte, versão, SHA-256 e indicação de privacidade obrigatória |
| `validacoes` e `alertas` | Resultado dos controles executados e limitações |

O filtro local pode bloquear padrões de manipulação; depois da recuperação, o filtro pela API analisa pergunta e fontes antes da resposta. Dados pessoais reconhecidos por padrões são mascarados, e indícios de informação pessoal de saúde são retidos. Essas heurísticas têm limites e podem causar falsos positivos ou negativos. Uma citação literal válida não comprova suporte semântico integral; a revisão humana permanece necessária para avaliar a qualidade.

Todas as execuções do aplicativo, incluindo diagnóstico, ajuda e falhas tratadas, tentam gerar HTML e JSON completos em `results/`, com nomes únicos. O caminho aparece no terminal. O HTML mostra resposta, fontes, validações e auditoria expansível; o JSON preserva configuração, prompts, respostas brutas mascaradas, latência, tokens e falhas. Na consulta, v1–v3 aparecem como não executadas; no comando `extrair`, o relatório compara as saídas das três versões. Se a pasta não puder ser escrita, o comando sinaliza erro no terminal; não é possível garantir um artefato em caso de interrupção abrupta ou falta de permissão. Relatórios locais não devem ser versionados.

Validação de integração em 23/11/2026: duas consultas sintéticas, quatro chamadas e custo estimado total de US$ 0,0005947, sem confirmação de fatura ou saldo. O primeiro resultado citou a regra crítica e exigiu revisão; o segundo identificou a orientação da v2026.3 como pendente. Isso não é o benchmark de 16 casos nem mede segurança absoluta ou acurácia de extração.

## Organização inicial

| Caminho | Finalidade |
| --- | --- |
| `pyproject.toml` | Metadados do pacote, requisito de Python e comando `extrator-ocorrencias` |
| `src/extrator_ocorrencia/config.py` | Caminhos, configuração local, modelo e parâmetros |
| `src/extrator_ocorrencia/cli.py` | Diagnóstico, consulta RAG e extração por argumento ou arquivo |
| `src/extrator_ocorrencia/extracao.py` | Prompts v1–v3, execução comparativa e validação da extração |
| `src/extrator_ocorrencia/base.py` e `rag.py` | Leitura do manifesto, integridade, trechos versionados e recuperação lexical |
| `src/extrator_ocorrencia/assistente.py` e `api.py` | Consulta em duas etapas e cliente centralizado da OpenAI |
| `src/extrator_ocorrencia/privacidade.py` e `relatorio.py` | Minimização, filtros e relatórios HTML/JSON |
| `tests/` | Testes locais com `unittest` |
| `data/documents/` | Base documental existente |
| `data/datasets/` | Casos de avaliação; contém apenas os casos complementares em `complementares/` |
| `docs/anexos/` | Anexo Word mencionado no histórico; indisponível nesta cópia |
| `data/examples/` | Seis perguntas sintéticas de demonstração, em `consultas_rag.jsonl` |
| `results/` | Relatórios e auditorias locais, ignorados pelo Git |

`data/examples/consultas_rag.jsonl` contém seis perguntas sintéticas com origem, versão e critério de recuperação, sem resultados inventados. Elas são separadas do benchmark principal e dos 71 casos complementares de extração. Em `results/`, somente `.gitkeep` é destinado ao versionamento; relatórios de execução permanecem locais e ignorados. Os casos complementares estão preparados, mas os 16 casos do benchmark principal ainda não foram criados nem congelados. Resultados selecionados para entrega deverão ser exportados e versionados explicitamente, após revisão de privacidade; a pasta local ignorada não constitui evidência entregue.
