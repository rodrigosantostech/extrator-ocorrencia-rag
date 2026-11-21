# Passo a passo — Extrator de Ocorrências com RAG

## Objetivo e situação atual

Construir um protótipo acadêmico que transforme mensagens informais da Rede Saúde Viva em ocorrências estruturadas, consulte o manual operacional e compare os prompts v1, v2 e v3 com evidências reproduzíveis.

**Decisão:** Python local no Windows e GPT pela API da OpenAI. Gemini e Colab aparecem somente no [documento original convertido](Trabalho_Final_MBA_Extrator_Ocorrencias.md), como referência histórica.

**Situação em 21/11/2026:** repositório clonado e documentação preparada. O protótipo, o dataset executável e o benchmark ainda precisam ser implementados. Python não foi encontrado pelo comando python --version nesta sessão; verificar o launcher py antes de instalar. Os percentuais e os status do Word não comprovam execução neste projeto.

**Metas:** pelo menos 90% de JSON sintaticamente válido e 80% de acurácia operacional, com as regras de cálculo abaixo. Uma avaliação com 16 casos oferece evidência limitada ao conjunto testado.

Checkpoint: **23/11/2026**. Entrega: **25/11/2026**. Confirmar horário e canal com o professor; o documento não os especifica.

## 1. Revisar os requisitos e fechar as regras

**Objetivo:** estabelecer o que será construído e como será avaliado, antes de ajustar prompts.

- [ ] Conferir R1–R5 e os limites do relatório e do pitch com o enunciado oficial da disciplina.
- [ ] Definir o usuário como coordenador de operações; usar mensagens sintéticas digitadas ou lidas de arquivo. Integração real com WhatsApp fica fora desta entrega.
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

## 3. Preparar manual, dataset e contrato de saída

**Depende de:** etapa 1; pode avançar antes da configuração da API.

- [ ] Extrair o manual completo da seção 5 para um arquivo de conhecimento, com versão e IDs de trechos.
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
- [ ] Para múltiplas ocorrências, priorizar a mais grave nesta primeira versão, conforme o caso 05.
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

## 6. Testar e medir as três versões

**Depende de:** etapas 4 e 5.

- [ ] Criar testes sem API para leitura do dataset, recuperação, validação, classificação de status e mascaramento.
- [ ] Testar loja ausente, loja desconhecida, múltiplas ocorrências, erro de digitação, sarcasmo, CPF/telefone/dado médico, resposta inválida e indisponibilidade da API.
- [ ] Executar os mesmos 16 casos em v1, v2 e v3, com o mesmo modelo e dados congelados.
- [ ] Verificar os quatro ataques originais e incluir testes complementares de fechamento de tags, instrução maliciosa em trecho recuperado e mensagem legítima com palavras suspeitas.
- [ ] Manter testes complementares separados do benchmark principal; não mudar o denominador silenciosamente.
- [ ] Avaliar justiça de forma exploratória com mensagens idênticas em que somente o nome muda; reconhecer a amostra limitada.

**Métricas e denominadores:**

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
- [ ] Desenhar o fluxo: mensagem → anonimização → filtro → recuperação → extração → validação → revisão humana.
- [ ] Justificar RAG pela atualização e rastreabilidade do manual. Evitar afirmar que todo fine-tuning exige GPUs próprias.
- [ ] Incluir declaração de uso de IA, referências oficiais verificadas, modelo utilizado e configuração do experimento.
- [ ] Diferenciar resultados observados de hipóteses e não prometer proteção absoluta nem conformidade jurídica comprovada.
- [ ] Revisar consistência entre relatório, tabelas, código e README.

**Concluído quando:** o relatório respeitar o limite de páginas e todas as afirmações quantitativas tiverem evidência.

## 8. Preparar o pitch, a demo e a entrega

**Depende de:** etapas 6 e 7.

- [ ] Ensaiar sete minutos: problema (1 min), solução (1,5 min), demo (2,5 min), resultados (1 min), conclusão (1 min).
- [ ] Demonstrar uma mensagem com gíria, uma sem loja e um ataque bloqueado, usando o protótipo Python local.
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
| 24/11/2026 | Etapas 6–7 | Benchmark real, testes e relatório |
| 25/11/2026 | Etapa 8 | Demo, vídeo, pitch e entrega |

Este cronograma é uma proposta de trabalho. Nenhuma etapa está concluída apenas por constar na tabela; marcar os itens somente após verificar seus critérios.
