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

## 3. Preparar manual, dataset e contrato de saída

**Depende de:** etapa 1; pode avançar antes da configuração da API.

**Registro de 21/11/2026 — origem: arquivo manual_operacoes_saude_viva.txt fornecido pelo usuário:** primeiro documento convertido para [data/documents/manual_operacoes_saude_viva.md](../data/documents/manual_operacoes_saude_viva.md), mantendo a versão 2026.1 e as regras originais. O arquivo inicia a estrutura data/documents/ sugerida em TRABALHO_MBA.md. IDs de trechos, recuperação e dataset continuam pendentes; a etapa 3 permanece aberta. A seção 3 de TRABALHO_MBA.md foi alinhada a esta inclusão e ao esclarecimento do usuário de 21/11/2026; a etapa 3 permanece aberta.

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
