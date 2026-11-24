# Passo a passo — Extrator de Ocorrências com RAG

## Objetivo e situação atual

Construir um protótipo acadêmico que transforme mensagens informais da Rede Saúde Viva em ocorrências estruturadas, consulte o manual operacional e compare os prompts v1, v2 e v3 com evidências reproduzíveis.

**Referência de solução — 21/11/2026, origem: esclarecimento do usuário nesta conversa:** o arquivo [Trabalho_Final_MBA_Extrator_Ocorrencias.md](Trabalho_Final_MBA_Extrator_Ocorrencias.md) representa aproximadamente o que queremos fazer. Usar seu problema, fluxo de extração e triagem, evolução v1–v3, manual, 16 casos e propostas de relatório/pitch como guia adaptável. Isso não aprova automaticamente todos os detalhes nem comprova resultados. As exigências acadêmicas estão em [TRABALHO_MBA.md](TRABALHO_MBA.md); as adaptações e decisões operacionais ficam neste passo a passo.

**Decisão:** Python local no Windows e GPT pela API da OpenAI. Gemini e Colab aparecem somente no [documento original convertido](Trabalho_Final_MBA_Extrator_Ocorrencias.md), como referência histórica.

**Situação em 21/11/2026:** repositório clonado e documentação preparada. O protótipo, o dataset executável e o benchmark ainda precisam ser implementados. Python não foi encontrado pelo comando python --version nesta sessão; verificar o launcher py antes de instalar. Os percentuais e os status do Word não comprovam execução neste projeto.

**Metas:** pelo menos 90% de JSON sintaticamente válido e 80% de acurácia operacional, com as regras de cálculo abaixo. Uma avaliação com 16 casos oferece evidência limitada ao conjunto testado.

Checkpoint: **23/11/2026**. Entrega: **25/11/2026**. Confirmar horário e canal com o professor; o documento não os especifica.

## Objetivo operacional e revisão de escopo — 21/11/2026

**Origem: esclarecimento do usuário nesta conversa.** A área acompanha ocorrências em lojas, como assaltos e outros incidentes, recebidas pelo WhatsApp. O objetivo é processar o conjunto de mensagens e consolidar os relatos. O plano anterior detalhava a extração por mensagem, mas não previa explicitamente associação de relatos, atualizações e consolidação; este registro complementa essa direção.

**Objetivo vigente:** transformar mensagens textuais em uma visão consolidada por loja, gravidade e período, preservando fontes, incidentes distintos e pendências. A Rede Saúde Viva é o cenário fictício de demonstração. RAG recupera regras do manual para fundamentar classificação e ação; associar mensagens e manter o consolidado são etapas adicionais do pipeline.

**Recorte proposto:** validar o fluxo com lotes sintéticos digitados ou lidos de arquivo. A conexão automática ao WhatsApp permanece evolução proposta, sem provedor ou mecanismo definido. Consolidar mensagens importadas não comprova captura de todas as mensagens do canal. Áudios e imagens ficam fora deste recorte textual.

**Fluxo planejado:** lote → identificação e mascaramento → triagem → extração por versão (RAG no v3) → validação → associação e atualizações → consolidado → revisão humana.

## 1. Revisar os requisitos e fechar as regras

**Objetivo:** estabelecer o que será construído e como será avaliado, antes de ajustar prompts.

- [ ] Conferir R1–R5 e os limites do relatório e do pitch com o enunciado oficial da disciplina.
- [ ] Detalhar o fluxo do coordenador de operações, usuário-alvo adotado como direção do projeto a partir da referência; usar mensagens sintéticas digitadas ou lidas de arquivo. A integração automática ao WhatsApp permanece uma evolução proposta; validar nesta entrega a consolidação de lotes sintéticos que representem o canal.
- [ ] Relacionar cada requisito à sua evidência:

| Requisito | Entregável | Evidência de conclusão |
| --- | --- | --- |
| R1 — Problema e valor | Problema, público e métricas | Metas e critérios definidos para o experimento |
| R2 — Prompts | v1, v2, v3 e registro das técnicas | Mesmos casos executados nas três versões |
| R3 — Personalização | Manual versionado e recuperação de trechos | Trechos recuperados registrados por consulta |
| R4 — Avaliação | 16 casos em JSONL e benchmark | Saídas brutas, métricas e falhas reproduzíveis |
| R5 — Segurança e ética | Defesas e matriz de riscos | Ataques, privacidade e limites documentados |
| Relatório e pitch | Até 8 páginas, 7 minutos e vídeo de reserva | Arquivos revisados e apresentação ensaiada |

- [ ] Registrar as divergências da fonte em um log de decisões, sem alterar silenciosamente a transcrição:

| Ponto | Tratamento para o protótipo |
| --- | --- |
| Caso 01 espera ALTO sem informar duração da falha de PDV; manual exige mais de 2 horas | Acrescentar “há 3 horas” à entrada do dataset executável e registrar a alteração |
| Caso 06 também omite duração | Acrescentar duração superior a 2 horas, preservando os erros de digitação |
| Caso 04 não comprova alagamento estrutural | Acrescentar evidência de comprometimento estrutural para sustentar CRÍTICO |
| Caso 02 fala em câmara fria sem dizer o conteúdo | Especificar vacinas ou insulinas para corresponder à regra CRÍTICO |
| Caso 11 apresenta override como ataque, mas descreve somente tags ignoradas | Definir bloqueio no v3 como resultado esperado, assim como nos casos 08–10 |
| Casos 12 e 13 são rotulados como regiões distintas, mas ambas as lojas são de SP | Tratar como teste exploratório de nomes; não afirmar cobertura de viés regional |
| null em v2 e “NÃO INFORMADO” em v3 | Preservar as versões; normalizar ambos apenas na comparação de campos ausentes |
| Prompt v3, código de exemplo e texto citam campos diferentes | Usar os seis campos do prompt v3; avaliar campos comuns às versões separadamente |
| Juiz LLM menciona resumo, ausente do JSON | Avaliar acao_necessaria com rubrica documentada; não inventar um campo resumo |
| Fonte anuncia 100% de proteção e resultados alcançados | Substituir por resultados medidos no relatório final; limitar conclusões aos testes |

**Concluído quando:** matriz e decisões estiverem registradas, com os casos ajustados identificados e sem métricas apresentadas como medidas antecipadamente.

## 2. Preparar Python e acesso à OpenAI

**Depende de:** etapa 1.

- [ ] Verificar py --version e python --version; instalar Python 3.12 caso não haja uma instalação utilizável.
- [ ] Na raiz do projeto, criar um ambiente virtual e usar seu executável diretamente:

~~~powershell
cd C:\Dev\extrator-ocorrencia-rag
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
~~~

- [ ] Criar dependências com SDK oficial da OpenAI, validação de dados, recuperação lexical e testes. Fixar as versões efetivamente validadas.
- [ ] Criar .gitignore antes de configurar credenciais: excluir .venv/, .env, caches e arquivos locais com segredos.
- [ ] Configurar OPENAI_API_KEY por variável de ambiente ou arquivo local ignorado pelo Git. Um eventual .env.example deve conter somente nomes e valores fictícios.
- [ ] Confirmar acesso e orçamento da API; não presumir créditos a partir da assinatura do chat.
- [ ] Consultar a documentação oficial vigente e escolher um modelo GPT acessível à conta, com saída estruturada e custo adequado. Registrar o identificador e manter o mesmo modelo nas três versões, com parâmetros comuns suportados.
- [ ] Validar uma chamada mínima antes do benchmark, sem imprimir a chave.

**Concluído quando:** ambiente e dependências forem reproduzíveis e a chamada mínima funcionar com modelo e configuração registrados.

### Base Python — 21/11/2026

**Origem:** solicitação do usuário para estruturar o projeto e, em seguida, adiar a etapa da chave. Acréscimo operacional à etapa 2; as etapas completas permanecem pendentes.

- Criados pacote instalável em `src/extrator_ocorrencia/`, manifesto `pyproject.toml`, comando de diagnóstico do manual e configuração centralizada de caminhos. O requisito inicial é Python 3.12 ou superior, com preparação orientada para 3.12.
- A estrutura usa somente a biblioteca padrão para permitir desenvolvimento local sem credenciais. A API, o modelo, seus parâmetros e as bibliotecas de validação e TF-IDF serão definidos ou integrados nas etapas correspondentes. Não foram fixadas versões de dependências ainda não validadas.
- Criados `.gitignore`, `.env.example` sem credenciais, seis testes locais e pastas reservadas para casos, exemplos e resultados. O código não carrega `.env` nem realiza chamadas externas.
- Validação local: Python 3.12.10 instalado para o usuário, ambiente `.venv` criado e pacote 0.1.0 instalado com `pip install -e .`. Os seis testes passaram; o diagnóstico por módulo e pelo comando instalado retornou `OK`, com leitura de 1.612 caracteres do manual. Esses resultados medem apenas os componentes locais implementados.
- A leitura do manual não comprova recuperação RAG, classificação, segurança operacional ou consolidação. Os 16 casos continuam pendentes; nenhuma métrica de extração foi medida.
- Rastreabilidade: preparação parcial de E1; organização inicial para R3, R4 e R5. R1 e R2 e os entregáveis E2–E4 não foram implementados nesta mudança.

### Verificação pontual de acesso à API — 23/11/2026

**Origem:** solicitação do usuário para verificar a disponibilidade da API, priorizando um modelo simples e econômico, e confirmação de que a chave estava disponível no `.env`. Registro operacional de preparação parcial de E1; não comprova R2–R5 nem conclui a etapa 2.

- Ambiente validado: Python 3.12.10 e SDK oficial `openai==3.58.0`, instalado na `.venv` e incluído no manifesto. O `.env` existente permaneceu ignorado pelo Git; seu conteúdo não foi alterado nem exibido.
- Modelo selecionado para esta verificação: `gpt-6-luna`, pela Responses API, com `reasoning.effort=none`, `max_output_tokens=64`, `store=false`, JSON Schema estrito, tempo limite de 30 segundos e nenhuma repetição automática. A configuração utilizada deve ser centralizada ao integrar a API ao aplicativo; não foi definido um snapshot datado para o benchmark.
- Fonte de preço e recursos: [documentação oficial do GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), consultada em 23/11/2026. Preço padrão publicado: US$ 0,10 por milhão de tokens de entrada e US$ 0,50 por milhão de saída. Escolha econômica para iniciar; qualidade operacional ainda precisa ser avaliada.
- Uma chamada com entrada sintética de conectividade foi concluída; resposta estruturada `{"status":"OK"}` validada. Uso medido: 46 tokens de entrada, 14 de saída e nenhum token de raciocínio; latência de 3,356 segundos. Estimativa: `(46 × 0,10 + 14 × 0,50) / 1.000.000 = US$ 0,0000116`, sem descontos de cache. Não representa fatura confirmada nem consulta de saldo ou limite financeiro.
- Evidências locais: `results/verificacao_api_20261123_191004.html` e `.json`, com configuração, entrada, resposta bruta, validação e uso. Verificação pontual em `results/verificar_api_local.py`; esses artefatos são ignorados e não compõem a implementação distribuída.
- v1, v2, v3, RAG, benchmark principal e testes complementares não foram executados. O aplicativo ainda não carrega `.env` nem chama a API. A integração permanente, a geração automática do HTML nos comandos existentes e a reprodução por um comando versionado permanecem pendentes; nenhum checklist completo foi marcado.

### Assistente de consulta RAG — 23/11/2026

**Origem:** autorização do usuário nesta conversa para implementar um assistente de consulta à base RAG. Escopo operacional desta entrega: perguntas sobre o manual, com resposta fundamentada; não substitui a extração de ocorrências, a consolidação nem a comparação v1–v3.

- Implementado `consultar`, com pergunta por argumento ou uma consulta em arquivo UTF-8, limite de 6.000 caracteres, seleção explícita do manual e modo `--somente-recuperar`, sem API. `config.py` centraliza caminhos, leitura restrita do `.env`, modelo e parâmetros; variáveis do processo prevalecem. Não foram alterados o `.env` existente nem os documentos da base.
- Base padrão v2026.1: nove trechos, separados por loja, gravidade e privacidade, com IDs estáveis e SHA-256. Base opcional v2026.3: somente os nove blocos do Anexo B, sem indexar exemplos ou gabaritos. Fontes de versões distintas não são misturadas. Como a v2026.3 contém propostas pendentes, toda consulta que a utiliza exige revisão humana; sua seleção não aprova essas propostas.
- Implementado TF-IDF com frequência logarítmica, IDF suavizado `log((1 + N) / (1 + df)) + 1`, normalização L2 e cosseno na biblioteca padrão, sem dependência adicional de recuperação. Até três trechos com pontuação positiva e privacidade obrigatória; pontuação não equivale a confiança nem comprova suficiência.
- Cliente único da Responses API: `gpt-6-luna` por padrão, `reasoning.effort=none`, `max_output_tokens=900` por chamada, `store=false`, tempo limite de 30 segundos e nenhuma repetição automática. Configuração alternativa via `OPENAI_MODEL` exige compatibilidade com esses parâmetros e saída estruturada; não há fallback automático.
- Consulta em duas etapas: filtro de segurança e geração com trechos recuperados. Bloqueios locais e ausência de correspondência lexical podem encerrar sem API. JSON Schema na API e validação local de campos, IDs e citações literais; falha de citação retém a resposta e exige revisão. Validação literal não comprova suporte semântico integral.
- Contrato `consulta-rag-1`: entrada mascarada, estado, resposta, citações (`trecho_id` e `citacao`), revisão humana, fontes, validações e alertas. É independente dos seis campos da extração. Não atribui situação de incidente nem consolida mensagens.
- Implementados mascaramento por padrões, retenção de indícios de dado pessoal de saúde, filtros de manipulação e tratamento de falhas da API, resposta incompleta, recusa e JSON inválido. São mitigações limitadas, sujeitas a falsos positivos e negativos; não comprovam proteção absoluta nem conformidade jurídica.
- `diagnostico`, `consultar`, ajuda e falhas tratadas passam a gerar HTML e JSON em `results/`, com IDs únicos, configuração, versão do código e indicação de alterações locais, versões de prompts, manual e seu hash, entrada, respostas brutas mascaradas, contexto, latência, tokens e custo estimado quando disponíveis. Falta de permissão de escrita ou interrupção abrupta pode impedir a geração. HTML de execução permanece ignorado e não foi adicionado ao Git.
- Validação local: pacote reinstalado com `pip install -e .`; `pip check` sem dependências quebradas; 32 testes sem API aprovados, incluindo recuperação, estabilidade de IDs, fontes, injeção direta e indireta, mascaramento, citação inventada, configuração, falha do SDK, resposta incompleta, HTML escapado e preservação de auditoria. São testes complementares de implementação, sem denominador compartilhado com os 16 casos principais.
- Consultas reais de integração: (1) ação e prazo para assalto à mão armada, manual v2026.1, citação crítica validada e revisão humana; (2) regra sobre preço e estoque, v2026.3, citação RAG-07 validada e orientação identificada como pendente. Cada consulta usou duas chamadas. Uso total: 4.342 tokens de entrada e 321 de saída. Estimativa pelo preço padrão publicado: `(4.342 × 0,10 + 321 × 0,50) / 1.000.000 = US$ 0,0005947`, sem descontos de cache e sem confirmação de fatura ou saldo. Não é avaliação de extração.
- Evidências locais: `results/execucao_20261123_200007_6e70af55.html` e `.json`; `results/execucao_20261123_201805_835a4b02.html` e `.json`. A renderização do segundo HTML foi inspecionada no Edge; viewport móvel emulado de 390 px, largura do conteúdo de 390 px, âncoras válidas e caracteres UTF-8 íntegros. Capturas e impressão de conferência ficaram somente em `results/`.
- Rastreabilidade: implementação parcial de E1 e de recuperação de R3, com preparação de controles de R5. R1 permanece sem avaliação de valor; R2/E3 ainda dependem de v1–v3; R4 depende do dataset principal congelado e das execuções comparáveis; E2 e E4 permanecem pendentes. A recuperação de consulta implementada não conclui o v3 de extração nem os checklists completos das etapas 2, 3, 4, 5 e 5A.

### Base vigente v2026.3 e cobertura da consulta — 23/11/2026

**Origem:** esclarecimento do usuário nesta conversa: a base efetiva deve ser `manual_operacoes_saude_viva_v2026.3.md`, com autorização para gerar dados fictícios coerentes se houver lacunas. Esta orientação substitui a escolha anterior da v2026.1 como padrão do assistente; não altera requisitos do professor nem aprova silenciosamente todas as propostas operacionais do manual.

- `MANUAL_PADRAO=2026.3` centraliza a escolha. O caminho padrão de `Configuracao`, o diagnóstico, o argumento omitido em `consultar` e a função de consulta usam a mesma versão. A v2026.1 continua disponível somente por seleção explícita; a ausência do arquivo vigente não provoca retorno à base antiga.
- Identificada uma lacuna de cobertura: os nove blocos do Anexo B não contemplavam detalhes já existentes sobre pontuação, taxonomia e consolidação. O índice agora incorpora também texto literal das seções 2, 4, 5, 6, 7, 8, 9, 12 e 16, totalizando 189 trechos. Tabelas são divididas por linha, com cabeçalho no título, e os demais blocos preservam linhas completas. Título e texto participam do TF-IDF; códigos como TI-01 são normalizados para busca exata por termo. A auditoria identifica `tfidf-local-2`, seções, campos indexados e quantidade de trechos.
- Não foi necessário inventar regras nem completar cadastros: o conteúdo existente do manual foi suficiente para a ampliação. O arquivo fonte permaneceu idêntico, com SHA-256 `fc83c434b2221d1d5b6c9cf18633e3b56f043721a0f5018dfd3a442169457007`. Fontes históricas não foram misturadas. O Anexo A, exemplos calculados e gabaritos continuam fora da indexação; os IDs dos nove blocos compactos foram preservados.
- Acrescentadas seis perguntas sintéticas em `data/examples/consultas_rag.jsonl`, com identificação, versão, data, origem, seção e evidência literal esperadas. Cobrem base de score, reimportação, código TI-01, apelido de loja, correção de gravidade e presunção de culpa. São exemplos de consulta, separados dos 16 casos principais e dos 71 complementares de extração; suas expectativas não são resultados inventados.
- Verificação local: 36 testes aprovados, incluindo padrão único, ausência de retorno automático à v2026.1, IDs únicos, literalidade dos trechos no arquivo fonte e recuperação da evidência esperada nas seis perguntas. Isso avalia a recuperação local dessas perguntas, sem medir a qualidade geral da geração nem executar o benchmark.
- Validação real sem `--manual`: consulta sobre a base do score do nível ALTO usou a v2026.3, respondeu 55 e citou literalmente `| ALTO | 55 | 55 a 79 |`, trecho `V2026.3-S08-004`, com revisão humana. Foram duas chamadas, 2.201 tokens de entrada e 123 de saída; custo estimado de `(2.201 × 0,10 + 123 × 0,50) / 1.000.000 = US$ 0,0002816`, sem confirmação de cobrança. Evidências: `results/execucao_20261123_210822_a53988cd.html` e `.json`. O diagnóstico confirmou leitura da v2026.3, com 67.404 caracteres, e gerou `results/execucao_20261123_210816_ec1b9cfb.html` e `.json`.
- Rastreabilidade: manutenção de E1 e ampliação da cobertura de R3; preservadas as restrições de dados sintéticos de R5. Não se concluem R2, R4, E2–E4, extração v1–v3 ou consolidação pela simples troca da base.

### Manual modular e remoção da versão antiga — 23/11/2026

**Origem:** esclarecimento do usuário nesta conversa: dividir a v2026.3 e remover o outro manual, a v2026.1. A organização documental abaixo substitui a leitura do arquivo único; não modifica regras operacionais nem requisitos do professor.

- A v2026.3 foi dividida em 12 documentos por assunto em `data/documents/manual_v2026_3/`, com título, versão, data, origem, natureza, público e escopo. Todos os corpos originais, inclusive seções de avaliação e exemplos, foram preservados literalmente. O manifesto registra arquivos, partes, ordem original, hashes e seções utilizadas pela recuperação.
- A fonte integral foi arquivada em `docs/referencias/manual_operacoes_saude_viva_v2026.3.md`, fora do índice, com o mesmo SHA-256 `fc83c434b2221d1d5b6c9cf18633e3b56f043721a0f5018dfd3a442169457007`. O antigo `data/documents/manual_operacoes_saude_viva.md`, v2026.1, foi excluído conforme solicitado. Sua recuperação permanece no histórico do Git; nenhuma alteração de histórico foi feita.
- A divisão foi conferida por reconstrução integral do documento original, antes da remoção dos arquivos da base ativa. Os 189 trechos mantiveram IDs, títulos, textos, versões, seções e indicação de privacidade. Nas seis perguntas sintéticas de conferência, IDs e pontuações dos resultados permaneceram iguais, com tolerância numérica de 1e-12. Evidência local: `results/validacao_migracao_manual.json`. A divisão física organiza a manutenção; não foi medida melhoria de qualidade por essa alteração.
- `base.py` valida versão, nomes de arquivo, limites de diretório, hashes e delimitadores do conteúdo. O RAG usa somente o que o manifesto permite; exemplos e documentos de avaliação não passam a ser evidência operacional. O diagnóstico confere todos os documentos. A CLI aceita apenas `--manual 2026.3`; a base não depende mais do arquivo antigo nem do arquivo integral arquivado.
- Cada trecho passa a identificar o documento do assunto e seu hash. `manual_sha256` identifica o manifesto, cujos registros identificam os documentos; `original_sha256` preserva a identificação da fonte integral no diagnóstico. Alterações posteriores exigem revisão e atualização do hash correspondente no manifesto, conforme README.
- Validação: 35 testes locais sem API aprovados após a adaptação dos testes para o manual modular; conferidas recuperação, citações, segurança, documentos ausentes, divergência de hash e caminhos indevidos. Recuperação local após a remoção encontrou `V2026.3-S08-004` em `manual_v2026_3/05_prioridade.md`. HTML e JSON: `results/execucao_20261123_212659_ccbd7f50.html` e `.json`. Nenhuma nova chamada à API foi necessária para essa conferência.
- Referências anteriores à v2026.1 e ao caminho antigo da v2026.3 neste histórico descrevem estados passados. O documento protegido `docs/TRABALHO_MBA.md` permanece inalterado, inclusive suas referências históricas; o estado atual da base é o deste registro e do README. A versão Word também permanece uma referência da transcrição original.
- Rastreabilidade: manutenção de E1, organização e auditabilidade de R3 e preservação dos limites de R5. R2, R4 e E2–E4 permanecem pendentes; não houve execução do benchmark nem consolidação de mensagens nesta migração.

### Relatório HTML — 23/11/2026

**Origem:** solicitação do usuário nesta conversa. Regra operacional complementar para a apresentação de resultados de E1 e apoio à demonstração de E4; não modifica os requisitos do professor.

- Registrada em `AGENTS.md` e `CLAUDE.md` a obrigação de gerar relatório HTML local ao término de cada execução do aplicativo Python, incluindo resultados e falhas tratadas, com mascaramento e escape de conteúdo externo.
- Relatórios devem ficar em `results/` e nunca ser enviados ao repositório. O `.gitignore` bloqueia arquivos `.html`, inclusive com letras maiúsculas na extensão, e permite somente `docs/examples/resultado_exemplo.html`, exemplo sintético e sem resultados medidos.
- Complemento solicitado pelo usuário em 23/11/2026: o HTML deve apresentar o resultado completo, com identificação e configuração, comparação v1–v3, técnicas, saídas possíveis, detalhe de casos, fontes e validações, consolidado e histórico, métricas com denominadores, segurança e auditoria. O exemplo passa a cobrir essas seções, com dados demonstrativos e versões não executadas explicitamente identificados. Regras equivalentes registradas nos dois arquivos de instruções; nenhuma avaliação foi executada nesta revisão.
- Verificação do exemplo ampliado: 11 seções com âncoras válidas, 16 casos de referência separados em 12 operacionais e 4 ataques, cinco blocos JSON parseáveis, citação e ação demonstrativas presentes literalmente no manual. Filtros, busca sem distinção de acentos e expansão/restauração para impressão conferidos com Node; apresentação renderizada no Edge e captura inspecionada. Essas verificações avaliam somente o HTML de exemplo, não o protótipo nem o benchmark.
- Preferência visual confirmada pelo usuário em 23/11/2026: layout bonito e profissional passa a ser obrigatório, com hierarquia tipográfica, cores consistentes, cartões, tabelas, responsividade, acessibilidade e impressão organizada. Exemplo refinado em CSS local; preservar o resultado completo é parte do critério de apresentação.
- Esta alteração registra a regra e prepara a política de versionamento. A geração automática de HTML no comando `diagnostico` ainda precisa ser implementada; o código atual continua imprimindo JSON no terminal.

## 3. Preparar manual, dataset e contrato de saída

**Depende de:** etapa 1; pode avançar antes da configuração da API.

**Registro de 21/11/2026 — origem: arquivo manual_operacoes_saude_viva.txt fornecido pelo usuário:** primeiro documento convertido para [data/documents/manual_operacoes_saude_viva.md](../data/documents/manual_operacoes_saude_viva.md), mantendo a versão 2026.1 e as regras originais. O arquivo inicia a estrutura data/documents/ sugerida em TRABALHO_MBA.md. IDs de trechos, recuperação e dataset continuam pendentes; a etapa 3 permanece aberta. A seção 3 de TRABALHO_MBA.md foi alinhada a esta inclusão e ao esclarecimento do usuário de 21/11/2026; a etapa 3 permanece aberta.

**Registro de 21/11/2026 — origem: arquivos fornecidos pelo usuário (Manual_Operacoes_Extrator_Saude_Viva_v2026.2.docx, grupo_whatsapp_ocorrencias.txt e casos_de_teste_adicionais.jsonl) e solicitação de adequação nesta conversa:**

- Incluído [data/documents/manual_operacoes_saude_viva_v2026.3.md](referencias/manual_operacoes_saude_viva_v2026.3.md), adequação da v2026.2 elaborada pelo usuário. A versão do Word está em [docs/anexos/](anexos/). Regras do v2026.1 permanecem marcadas; regras novas estão identificadas como PROPOSTA v2026.2 ([P]) ou PROPOSTA v2026.3 ([P3]) e aguardam validação.
- Adequações ao repositório: Python com API da OpenAI e TF-IDF no lugar de Colab, status do pipeline separado (extraído, revisão, bloqueio, sem ocorrência e erro técnico), citação literal em regra_consultada, rubrica de acao_necessaria desta etapa 6 (4, 4 e 2), métricas com denominadores, remoção de percentuais não medidos, decisões 4 e 7 alinhadas a este passo a passo e seção 16 com os critérios da etapa 5A.
- Ampliações propostas: consultas de preço, procura de produtos em outras lojas, intrusão, novos cenários de assalto, furto e arrastão, catálogo de 36 tipos, trechos identificados para recuperação (Anexo B) e 17 decisões pendentes, das quais 9 são novas.
- Incluídos 71 casos complementares (IDs 17 a 87) em [data/datasets/complementares/](../data/datasets/complementares/), separados do benchmark principal: casos_de_teste_adicionais.jsonl, a exportação sintética grupo_whatsapp_ocorrencias.txt gerada a partir dos casos e gabarito_consolidacao_lote.json, com destino de cada mensagem, 60 ocorrências esperadas, vínculos, reincidências e contagens.
- Correções nos casos fornecidos: horários dos casos 17 e 27 coerentes com a duração relatada; caso 48 acrescentado porque a retratação do caso 46 não tinha aviso correspondente; ação do caso 25 alinhada à matriz do MODERADO, com divergência registrada como decisão pendente 11; ocorrências secundárias dos casos 25, 26, 64 e 78 preservadas no consolidado.
- Verificação local, sem API: script PowerShell conferiu JSON, campos, lojas canônicas, gravidades, presença literal dos trechos no manual, revisão obrigatória dos CRÍTICOS, ausência de CPF, telefone e nomes de clientes nas saídas esperadas, vínculos, reincidências e contagens do gabarito, com 0 erros. O Word abriu o .docx gerado. Os testes Python não foram executados nesta sessão porque o Python não estava instalado na máquina utilizada.
- Os casos não foram executados em nenhuma versão de prompt e não produzem métrica. Os 16 casos do benchmark principal continuam pendentes de conversão e congelamento; o diagnóstico do CLI continua lendo o manual v2026.1. A escolha do manual indexado pelo RAG permanece pendente até a validação das propostas.
- Rastreabilidade: preparação documental para R3 (base RAG), R4 (casos complementares e avaliação da consolidação) e R5 (ataques, LGPD e equidade). Nenhum requisito é declarado atendido por esta inclusão.

- [ ] Conferir o manual já preparado com a fonte e acrescentar IDs de trechos, preservando versão e regras.
- [ ] Converter os 16 casos da seção 6 para casos_de_teste.jsonl, aplicando e documentando as decisões da etapa 1.
- [ ] Para cada caso, registrar ID, categoria, entrada, resultado esperado, campos avaliáveis e regra que fundamenta a expectativa.
- [ ] Congelar o conjunto antes de medir v1–v3. Usar exemplos de desenvolvimento separados para ajustes posteriores.

**Contrato planejado de extração:**

| Campo | Regra |
| --- | --- |
| loja | Nome canônico quando reconhecido; “NÃO INFORMADO” se ausente |
| tipo_ocorrencia | Descrição breve baseada na mensagem |
| gravidade | CRÍTICO, ALTO, MODERADO ou BAIXO, conforme manual |
| acao_necessaria | Ação fundamentada na regra recuperada |
| responsavel_contato | Pessoa explicitamente citada; “NÃO INFORMADO” se ausente |
| regra_consultada | Trecho literal do manual no v3, verificado em código |

- [ ] Preservar uma loja desconhecida como relatada e emitir alerta separado de “loja fora do cadastro”; não convertê-la em loja conhecida.
- [ ] Na ausência de evidência para gravidade ou regra, encaminhar para revisão humana sem inventar classificação.
- [ ] Preservar a prioridade da ocorrência mais grave no benchmark individual, conforme o caso 05. No consolidado, preservar também os incidentes secundários; priorizar determina a ordem de apresentação, sem autorizar descarte. Avaliar essa ampliação em casos complementares.
- [ ] Separar extração de controle do pipeline: extraído, bloqueado, revisão necessária ou erro técnico. Um bloqueio não precisa conter campos de ocorrência.
- [ ] Restringir o dataset a dados fictícios; incluir exemplos sintéticos de CPF, telefone e dado médico para testar anonimização.

**Concluído quando:** houver 16 linhas JSON válidas, IDs únicos e expectativas coerentes com o manual.

## 4. Implementar v1 e v2 e preparar o checkpoint

**Depende de:** etapas 2 e 3.

- [ ] Criar um comando local para processar uma mensagem e outro para executar o dataset por versão.
- [ ] Implementar v1 como baseline zero-shot, preservando a resposta bruta. Não forçar saída estruturada nessa versão.
- [ ] Implementar v2 com persona, few-shot e formato estruturado. Documentar que a comparação envolve tanto prompt quanto restrição de saída da API.
- [ ] Centralizar cliente da API, modelo e parâmetros para evitar diferenças acidentais entre versões.
- [ ] Tratar timeout, recusa, resposta vazia ou inválida e erro da API sem registrar credenciais; limitar tentativas e contabilizar falhas.
- [ ] Salvar por execução: ID do caso, versão, modelo, data, parâmetros, resposta, erro, latência e uso de tokens quando disponível.
- [ ] Executar os 16 casos em v1 e v2 e produzir tabela inicial, sem corrigir manualmente as respostas medidas.

**Para o checkpoint de 23/11:** levar v1/v2 funcionando, dataset, tabela inicial, arquitetura prevista para v3 e divergências identificadas. Perguntar se a avaliação da ação deve priorizar completude ou concisão e como apresentar a comparação entre prompt livre e saída estruturada.

**Concluído quando:** uma pessoa conseguir reproduzir v1/v2 e rastrear a tabela até as saídas salvas.

## 5. Implementar recuperação e v3 defensivo

**Depende de:** etapas 3 e 4.

- [ ] Dividir o manual em trechos por unidade, classificação e privacidade, preservando IDs e versão.
- [ ] Para esta base pequena, implementar recuperação lexical local com TF-IDF e similaridade de cosseno; normalizar aliases de lojas antes da busca.
- [ ] Recuperar os três trechos mais relevantes com pontuação positiva e incluir a política de privacidade como contexto obrigatório. Registrar IDs e pontuações; contexto insuficiente deve gerar revisão.
- [ ] Não apresentar a simples inclusão do manual inteiro como uma recuperação já implementada.
- [ ] Executar v3 em duas etapas: filtro de segurança e, quando aprovado, extração com trechos recuperados.
- [ ] Tratar mensagem e documentos recuperados como dados não confiáveis. Delimitadores XML ajudam na organização, mas não garantem proteção.
- [ ] Mascarar CPF, telefone pessoal e informações médicas sintéticas antes do envio; validar novamente a saída e evitar persistir texto sensível bruto.
- [ ] Validar JSON em código, existência da loja, presença da citação no manual e coerência da gravidade com a evidência.
- [ ] Encaminhar bloqueios, incertezas e casos críticos à revisão humana. O protótipo não deve acionar pessoas ou sistemas externos automaticamente.

**Concluído quando:** a ocorrência vier acompanhada dos trechos usados, dados ausentes não forem inventados e ataques produzirem resultados auditáveis.

## 5A. Consolidar lotes de mensagens

**Depende de:** contratos da etapa 3 e extração validada das etapas 4–5. Proposta operacional para atender ao objetivo confirmado, sem modificar silenciosamente os 16 casos ou os prompts históricos.

- [ ] Definir entrada com ID da mensagem, origem/conversa fictícia, data/hora com fuso quando disponível, texto sintético e referência à mensagem respondida quando disponível. Registrar metadados ausentes; não exigir telefone real.
- [ ] Manter os seis campos de extração e acrescentar metadados separados: ID da ocorrência, IDs das mensagens-fonte, histórico, situação relatada, alertas e estado da revisão. Separar situação do incidente de status técnico.
- [ ] Dar destinação a todas as mensagens importadas: vinculada a ocorrência, sem ocorrência identificada, bloqueada, revisão necessária ou erro técnico. Falhas e mensagens sem ocorrência devem aparecer nas contagens.
- [ ] Reimportar a mesma mensagem por origem e ID sem duplicar ocorrência ou contagem. Textos iguais com IDs diferentes não comprovam duplicidade de evento.
- [ ] Associar relatos somente com evidência compatível de loja, evento e vínculo explícito ou temporal documentado. Definir e versionar critérios e janela temporal antes dos testes. Mesmo tipo de problema na mesma loja, isoladamente, não comprova um único incidente.
- [ ] Encaminhar vínculo ambíguo para revisão; não misturar lojas ou conversas sem relação comprovada. Uma resposta pode complementar dados ausentes apenas com vínculo verificável e fonte registrada.
- [ ] Incorporar complementos, correções e resolução explicitamente relatados, sem apagar histórico ou gravidade anteriormente registrada. Contradições geram pendência; silêncio não significa resolução.
- [ ] Preservar ocorrências distintas na mesma mensagem. Destacar a mais grave e manter as secundárias ligadas à fonte.
- [ ] Gerar consolidado por período e loja, ordenado por gravidade, com resumo factual, ação e regra, situação relatada, pendências e mensagens-fonte. Contar ocorrências únicas separadamente de mensagens.
- [ ] Explicitar data de corte e mensagens sem data fora do filtro temporal. Exibir bloqueios, revisões e erros separadamente. Não inventar fatos, responsáveis, ações executadas ou resolução.
- [ ] Permitir revisão humana de associações e registrar correções. Aplicar mascaramento também ao histórico, metadados textuais e arquivos exportados; somente dados sintéticos neste protótipo.

**Exemplo sintético de aceite:** m01 informa “Loja 02: assalto à mão armada agora”; m02 responde explicitamente a m01: “equipe em segurança; atendimento suspenso”; m03 informa “Loja 03: preciso de papel”. Esperar duas ocorrências, com m01/m02 ligadas ao assalto e m03 separada. A resposta não comprova resolução. Reimportar m02 não aumenta a quantidade de ocorrências. Classificação e ação devem seguir o manual, com citação no v3.

**Concluído quando:** um lote produzir consolidado reproduzível, todas as mensagens tiverem destinação e cada ocorrência puder ser rastreada às fontes, sem descarte de incidentes secundários, fusões indevidas ou duplicação por reimportação, conforme os casos complementares.

## 6. Testar e medir as três versões

**Depende de:** etapas 4, 5 e 5A; o benchmark individual pode ser executado antes da consolidação.

- [ ] Criar testes sem API para leitura do dataset, recuperação, validação, classificação de status e mascaramento.
- [ ] Testar loja ausente, loja desconhecida, múltiplas ocorrências, erro de digitação, sarcasmo, CPF/telefone/dado médico, resposta inválida e indisponibilidade da API.
- [ ] Executar os mesmos 16 casos em v1, v2 e v3, com o mesmo modelo e dados congelados.
- [ ] Verificar os quatro ataques originais e incluir testes complementares de fechamento de tags, instrução maliciosa em trecho recuperado e mensagem legítima com palavras suspeitas.
- [ ] Manter testes complementares separados do benchmark principal; não mudar o denominador silenciosamente.
- [ ] Avaliar justiça de forma exploratória com mensagens idênticas em que somente o nome muda; reconhecer a amostra limitada.

**Avaliação complementar da consolidação — separada dos 16 casos:**

- [ ] Preparar e congelar lotes com relato fragmentado, atualização, reimportação, textos iguais de eventos distintos, conversas intercaladas, múltiplas lojas, duas ocorrências na mesma mensagem, conflito, loja/data ausente e mensagem sem ocorrência.
- [ ] Incluir assalto à mão armada e incidente sem evidência suficiente para enquadramento. Não generalizar todo incidente como CRÍTICO sem suporte no manual.
- [ ] Anotar ocorrências e vínculos mensagem–ocorrência esperados, fatos a preservar e critérios de revisão. Definir correspondência entre ocorrências previstas e esperadas antes da medição.
- [ ] Verificar reimportação sem aumento de contagem, preservação dos incidentes secundários, revisão de vínculos ambíguos e fontes para cada fato do resumo.
- [ ] Medir cobertura de mensagens = mensagens com destinação / mensagens importadas; cobertura de ocorrências = ocorrências esperadas identificadas / ocorrências esperadas; precisão de ocorrências = ocorrências previstas corretamente identificadas / ocorrências previstas.
- [ ] Medir precisão de associação = vínculos corretos / vínculos produzidos; revocação de associação = vínculos esperados recuperados / vínculos esperados. Registrar fusões indevidas e fragmentações por lote.
- [ ] Medir rastreabilidade = ocorrências com fontes válidas / ocorrências produzidas; fidelidade do resumo = afirmações sustentadas nas mensagens / afirmações verificadas. Avaliar o suporte da regra à ação separadamente dos fatos relatados.
- [ ] Informar numerador e denominador; zero no denominador significa “não aplicável”. Fixar limiares agregados antes dos testes; ainda pendentes. Metas de extração não são metas automaticamente aprovadas de consolidação.
- [ ] Se comparar consolidados de v1–v3, usar os mesmos lotes e regras, distinguindo falhas de extração e associação. Preservar v1 bruta; eventual adaptação para consolidação deve ser documentada e não conta como saída nativa estruturada.

**Métricas e denominadores do benchmark individual:**

| Métrica | Como calcular |
| --- | --- |
| JSON sintaticamente válido | Respostas parseáveis / 16 casos, incluindo bloqueios em JSON; erros contam como falha |
| Conformidade de extração | Extrações válidas no schema / 12 casos operacionais; informar também quantas extrações foram produzidas |
| Acurácia operacional | Acertos em loja, gravidade e responsável / total desses campos anotados nos 12 casos operacionais |
| Acerto integral por caso | Casos com todos os campos-chave corretos / 12 casos operacionais |
| Resistência aos ataques | Ataques neutralizados sem cumprir a instrução maliciosa / 4 ataques |
| Falsos bloqueios | Mensagens operacionais bloqueadas / 12 casos operacionais |
| Privacidade e alucinação | Resultados por caso e tipo de dado, com falhas descritas |
| Custo e tempo | Tokens/custo quando disponíveis, latência e quantidade de chamadas por versão |

- [ ] Comparar nomes de loja por ID canônico; aceitar “NÃO INFORMADO” ou null apenas como equivalência de ausência na métrica, preservando o formato original.
- [ ] Registrar numerador e denominador. Não reutilizar percentuais do Word nem penalizar bloqueio correto por não conter campos de ocorrência.
- [ ] Para acao_necessaria, usar rubrica de 0–10: aderência ao manual (0–4), completude (0–4) e clareza (0–2). Fazer avaliação humana; juiz LLM é complemento opcional, com revisão humana e registro de modelo/prompt.
- [ ] Não conceder acerto com base em justificativa inventada. Registrar citação correta e ação adequada separadamente.
- [ ] Se houver correções após a primeira rodada, preservar os resultados anteriores e registrar nova rodada completa.

**Concluído quando:** os testes locais passarem e as tabelas puderem ser recalculadas a partir dos artefatos salvos, mesmo que as metas não sejam atingidas.

## 7. Montar o relatório final

**Depende de:** etapa 6.

- [ ] Escrever até oito páginas conforme a estrutura da seção 9 do documento.
- [ ] Explicar problema e valor, técnicas dos prompts, recuperação efetiva, metodologia, resultados medidos, segurança e limitações.
- [ ] Desenhar o fluxo completo: lote → identificação e mascaramento → filtro → recuperação → extração → validação → associação e atualizações → consolidado → revisão humana. Diferenciar importação de lotes de integração automática ao WhatsApp.
- [ ] Justificar RAG pela atualização e rastreabilidade do manual. Evitar afirmar que todo fine-tuning exige GPUs próprias.
- [ ] Incluir declaração de uso de IA, referências oficiais verificadas, modelo utilizado e configuração do experimento.
- [ ] Diferenciar resultados observados de hipóteses e não prometer proteção absoluta nem conformidade jurídica comprovada.
- [ ] Revisar consistência entre relatório, tabelas, código e README.

**Concluído quando:** o relatório respeitar o limite de páginas e todas as afirmações quantitativas tiverem evidência.

## 8. Preparar o pitch, a demo e a entrega

**Depende de:** etapas 6 e 7.

- [ ] Ensaiar sete minutos: problema (1 min), solução (1,5 min), demo (2,5 min), resultados (1 min), conclusão (1 min).
- [ ] Demonstrar lote com relatos e atualização do mesmo incidente, ocorrência em outra loja e reimportação sem duplicação; incluir gíria, ausência de loja e ataque bloqueado. Mostrar o consolidado e suas fontes no protótipo Python local.
- [ ] Usar somente percentuais medidos, com denominadores e limitações.
- [ ] Gravar vídeo de reserva de cerca de um minuto e preparar saídas salvas para falha de internet/API, identificando quando forem usadas.
- [ ] Atualizar o README com instalação, configuração, comandos implementados, execução dos testes e reprodução do benchmark.
- [ ] Conferir que a entrega não contém credenciais ou dados pessoais reais.
- [ ] Enviar protótipo e relatório no canal confirmado até 25/11/2026.

**Concluído quando:** os arquivos forem entregues, os comandos tiverem sido verificados e o pitch couber em sete minutos.

## Sequência sugerida

| Data | Prioridade | Resultado verificável |
| --- | --- | --- |
| 21/11/2026 | Etapas 1–3 | Regras alinhadas, ambiente preparado e dataset estruturado |
| 22/11/2026 | Etapa 4 e início da 5 | v1/v2 executados e recuperação iniciada |
| 23/11/2026 | Checkpoint e continuação da 5 | Feedback registrado e v3 implementado |
| 24/11/2026 | Etapa 5A e etapas 6–7 | Consolidado, benchmark individual, avaliação complementar e relatório |
| 25/11/2026 | Etapa 8 | Demo, vídeo, pitch e entrega |

Este cronograma é uma proposta de trabalho. Nenhuma etapa está concluída apenas por constar na tabela; marcar os itens somente após verificar seus critérios.
