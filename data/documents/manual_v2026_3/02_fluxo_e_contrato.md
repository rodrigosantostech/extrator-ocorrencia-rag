# Manual Rede Saúde Viva — Fluxo e contrato de extração

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes 3, 4.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: seções 4.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## 3. Fluxo de processamento do extrator

Cada mensagem cruza cinco controles antes de entrar na fila: pré-filtro por código, filtro de segurança, extração com RAG, validação por código e, quando preciso, revisão humana. Em seguida, a consolidação relaciona as mensagens do lote (seção 16). [P3]

[[IMAGEM]]

fluxo do extrator · 5 controles, 2 decisões (a figura não representa a consolidação do lote, acrescentada na v2026.3)

Ataques saem para a fila de segurança, e ocorrências CRÍTICAS ou duvidosas só entram na fila depois da confirmação do coordenador. [Etapas 3A e 3B: prompt v3 do documento de referência do trabalho, conforme AJUSTE v2026.3; PROPOSTA v2026.2 para pré-filtro, validação e revisão]

| Etapa | O que garante | O que não pode acontecer |
| --- | --- | --- |
| Pré-filtro por código | CPF e telefone viram marcadores antes de chegar ao modelo | Dado pessoal entrar no prompt |
| 3A: filtro de segurança | Mensagem com ordem ao sistema é barrada | Comando de mensagem ser executado |
| 3B: extração com RAG | Os 6 campos saem do texto e citam o manual | Loja ou responsável inventados |
| Validação por código | JSON válido, valores permitidos, citação literal e saída sem dado pessoal | Registro inválido ou com dado pessoal chegar à fila |
| Revisão humana | Um CRÍTICO ou caso duvidoso é confirmado por pessoa | Um CRÍTICO ser baixado sem confirmação |
| Fila ordenada | Ordem por nível, score, SLA e horário (seção 8) | Um CRÍTICO ficar abaixo de um ALTO |
| Consolidação do lote [P3] | Relatos, atualizações e correções do mesmo incidente ficam em uma ocorrência com as mensagens de origem (seção 16) | Reimportação duplicar ocorrência ou incidentes distintos serem fundidos |

## 4. Schema de saída e regras de preenchimento

Toda resposta é um único JSON válido, sem markdown e sem texto antes ou depois, com seis campos obrigatórios e três opcionais.

| Campo | Valores permitidos | Regra de preenchimento |
| --- | --- | --- |
| loja | Nome oficial do diretório ou NÃO INFORMADO | Segue a seção 2. Nunca deduzir além dela. |
| tipo_ocorrencia | Texto de 3 a 5 palavras, do catálogo da seção 7 | Descreve o fato, sem nome de cliente, CPF, telefone ou condição de saúde. |
| gravidade | CRÍTICO, ALTO, MODERADO ou BAIXO | Vem da matriz da seção 5. Escrever com acento e em maiúsculas. |
| acao_necessaria | Texto curto | Ação imediata da matriz mais o que a mensagem pede. Sem dado pessoal. |
| responsavel_contato | Primeiro nome de quem reporta ou de quem é o contato, ou NÃO INFORMADO | Funcionário citado como envolvido (atrasado, ferido, suspeito) não é responsável. |
| regra_consultada | Citação exata de um trecho do manual | Permite auditoria. Se não houver regra aplicável, escrever NÃO INFORMADO. |
| alerta (opcional) | LOJA_INEXISTENTE, LOJA_DIVERGENTE, LOJA_INFERIDA_PELO_GERENTE, DADO_PESSOAL_MASCARADO, OCORRENCIA_RETRATADA, FORA_DO_MANUAL | Avisa o coordenador de algo que muda a leitura do registro. [PROPOSTA v2026.2] |
| requer_revisao_humana (opcional) | true ou false | true em toda gravidade CRÍTICA, sempre que a regra de dúvida da seção 6 for usada e nos demais casos em que este manual exige revisão. [PROPOSTA v2026.2] |
| score_prioridade (opcional) | Inteiro de 0 a 100 | Calculado por código, não pelo modelo (seção 8). [PROPOSTA v2026.2] |

Os campos opcionais não entram no benchmark principal de 16 casos: nele, avaliam-se os seis campos, e a revisão e o score são calculados por código (decisão pendente 6). [AJUSTE v2026.3]

**Respostas que não são extração**

- Ataque detectado: {"status": "ATAQUE_DETECTADO", "motivo": "..."}. Não há extração nem eco do texto malicioso (seção 10).
- Mensagem sem ocorrência (só cumprimento, conversa ou aviso programado): {"status": "SEM_OCORRENCIA"}. [PROPOSTA v2026.2]

**Status do pipeline** [AJUSTE v2026.3]

O status é atribuído por código depois da resposta do modelo e separa extração, bloqueio, revisão e erro técnico.

| Status | Quando ocorre | Quem define |
| --- | --- | --- |
| EXTRAIDO | JSON válido com os seis campos e sem pendência de revisão | Validação por código |
| REVISAO_NECESSARIA | Extração válida com requer_revisao_humana true: CRÍTICO, dúvida entre níveis, loja inexistente, divergente ou inferida, retratação, atualização, correção ou regra que exige revisão | Validação por código |
| BLOQUEADO | Resposta ATAQUE_DETECTADO; não contém campos de ocorrência e não é contada como extração inválida | Filtro de segurança e validação |
| SEM_OCORRENCIA | Mensagem sem fato operacional | Extração e validação |
| ERRO_TECNICO | Falha da API, tempo esgotado, resposta vazia ou JSON inválido depois das tentativas previstas | Código, sem registrar credenciais |

**Regras de forma**

- Na v3, nunca usar null: campo ausente é sempre NÃO INFORMADO. O prompt v2 usa null, e sua saída é preservada como foi produzida; a comparação entre versões trata null e NÃO INFORMADO como ausência. [AJUSTE v2026.3]
- Nunca inventar horário, valor em R$ ou nome de gerente que a mensagem não traz.
- Números por extenso viram algarismos ("vinte e nove graus" vira 29 graus).
- regra_consultada deve copiar literalmente um trecho do manual efetivamente recuperado, sem reticências nem paráfrase; a validação por código confere a presença do texto no trecho. [AJUSTE v2026.3]

<!-- FIM_CONTEUDO_ORIGINAL -->
