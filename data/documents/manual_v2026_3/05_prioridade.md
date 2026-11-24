# Manual Rede Saúde Viva — Pontuação e prioridade

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes 8.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: seções 8.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## 8. Pontuação e ranking da fila

Cada ocorrência recebe um score de prioridade de 0 a 100, e a fila do coordenador é ordenada por ele. Todas as regras desta seção são PROPOSTA v2026.2.

**Como o score é calculado**

O score parte da base do nível e soma ajustes inteiros. Cada nível tem um teto, para que um BAIXO nunca passe de um MODERADO.

| Nível | Base | Faixa permitida |
| --- | --- | --- |
| CRÍTICO | 80 | 80 a 100 |
| ALTO | 55 | 55 a 79 |
| MODERADO | 30 | 30 a 54 |
| BAIXO | 10 | 0 a 29 |

| Ajuste | Pontos | Quando vale |
| --- | --- | --- |
| Pessoa ferida ou refém | +10 | A mensagem cita ferido, agredido ou refém. |
| Ocorrência em andamento | +5 | Fato no presente ("agora", "está parado", "ainda sem luz"). |
| Loja sem vender ou sem atender | +5 | PDV ou sistema fora, loja fechada, fila parada. |
| Produto sensível em risco | +5 | Vacinas, insulinas ou medicamentos controlados. |
| Loja não identificada | +3 | A loja precisa ser localizada com urgência. |
| Reincidência | +5 | Mesma loja e mesmo tipo nos últimos 7 dias (exige histórico). |

**Exemplos calculados**

| Caso | Gravidade | Cálculo | Score |
| --- | --- | --- | --- |
| 38 Assalto com funcionário ferido | CRÍTICO | 80 + 10 ferido + 5 em andamento | 95 |
| 59 Assalto com equipe retida no estoque | CRÍTICO | 80 + 10 refém + 5 em andamento | 95 |
| 23 Câmara de vacinas sem energia, loja não informada | CRÍTICO | 80 + 5 em andamento + 5 produto sensível + 3 loja não identificada | 93 |
| 37 Assalto armado, ninguém ferido, com assalto na mesma loja em 20/11 (caso 59) | CRÍTICO | 80 + 5 em andamento + 5 reincidência | 90 |
| 71 Intrusão em andamento com a loja fechada | CRÍTICO | 80 + 5 em andamento | 85 |
| 17 PDV parado há quase 3 horas | ALTO | 55 + 5 em andamento + 5 loja sem vender | 65 |
| 42 Furto de clonazepam | ALTO | 55 + 5 produto sensível | 60 |
| 18 Atraso de fornecedor | MODERADO | 30 | 30 |
| 22 Atraso de escala de 15 minutos | BAIXO | 10 | 10 |

A reincidência depende do histórico do lote: no registro individual, sem histórico, ela não é somada. [AJUSTE v2026.3]

**Ordem da fila**

- Nível de gravidade, de CRÍTICO para BAIXO.
- Score de prioridade, do maior para o menor.
- Menor tempo restante do SLA do nível (15 minutos, 4 horas).
- Horário da mensagem, da mais antiga para a mais recente.

Um CRÍTICO nunca pode aparecer abaixo de um ALTO. Se isso acontecer, o teste de ranking da seção 13 reprova a versão do prompt.

**Quem calcula**

O score é calculado por código Python a partir dos campos do JSON, não pelo modelo. Assim o mesmo registro sempre gera o mesmo número, e o prompt continua com os seis campos já testados nas versões v1 a v3.

**Rankings gerenciais**

Além da fila, o extrator alimenta três rankings semanais para o coordenador:

| Ranking | Critério | Para que serve |
| --- | --- | --- |
| Lojas com mais carga | Soma dos scores dos últimos 7 dias, mostrando o nome da loja | Onde concentrar visitas e apoio |
| Tipos mais frequentes | Contagem por código do catálogo (seção 7) | Onde atacar a causa, como PDV ou ar condicionado |
| Regionais com mais CRÍTICOS | Contagem de CRÍTICOS por regional | Onde reforçar a resposta de 15 minutos |

<!-- FIM_CONTEUDO_ORIGINAL -->
