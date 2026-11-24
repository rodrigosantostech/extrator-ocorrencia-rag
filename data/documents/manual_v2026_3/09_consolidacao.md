# Manual Rede Saúde Viva — Consolidação de mensagens

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes 16.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: seções 16.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## 16. Consolidação de mensagens do grupo

A consolidação reúne o lote importado em ocorrências únicas por loja, gravidade e período. Esta seção traduz para regras de consulta os critérios da etapa 5A do passo a passo do repositório; todos os itens são PROPOSTA v2026.3 e dependem da implementação e dos testes.

**Entrada esperada**

- Cada mensagem traz identificador, conversa, data e hora com fuso, remetente, texto e, quando houver, a mensagem respondida. Metadado ausente é registrado como ausente; não se exige telefone real.
- O arquivo grupo_whatsapp_ocorrencias.txt reproduz a exportação textual do grupo. O arquivo casos_de_teste_adicionais.jsonl traz os mesmos textos com identificador, fuso e resposta.

**Destino de cada mensagem**

| Destino | Quando |
| --- | --- |
| VINCULADA | A mensagem gera ou complementa uma ocorrência |
| SEM_OCORRENCIA | A mensagem não descreve fato operacional |
| BLOQUEADA | Ataque detectado; a mensagem vai para a fila de segurança |
| FORA_DO_FILTRO_TEMPORAL | A mensagem não tem data ou está fora do período consolidado |
| ERRO_TECNICO | Houve falha de processamento, contada separadamente |

Toda mensagem importada recebe exatamente um destino, e as contagens mostram cada destino separadamente.

**Critérios de associação**

- Vínculo explícito: resposta a uma mensagem anterior ou referência clara ao mesmo evento da mesma loja ("atualizando o assalto", "sobre o assalto de agora", "corrigindo").
- Vínculo candidato: mesma loja, mesmo tipo e intervalo de até 30 minutos, sem referência explícita. O vínculo é proposto e marcado para revisão humana (decisão pendente 13).
- Mesmo tipo de problema na mesma loja, por si só, não prova que se trata do mesmo incidente. Lojas e conversas diferentes nunca são unidas sem relação comprovada.
- Ocorrência com loja NÃO INFORMADO não é associada a ocorrência de loja conhecida, mesmo com DDD ou horário próximos.

**Atualizações, correções e retratações**

- Complemento, correção e resolução só entram quando relatados de forma explícita, e o histórico e a gravidade já registrados são preservados.
- Correção que reduz a gravidade e retratação de CRÍTICO geram pendência de revisão; a gravidade consolidada não cai sozinha.
- Silêncio não significa resolução: ocorrência sem novo relato continua aberta.

**Reimportação e textos iguais**

- Reimportar a mesma mensagem, com a mesma conversa e o mesmo identificador, não cria ocorrência nem altera contagens.
- Textos iguais com identificadores diferentes não comprovam duplicidade de evento (casos 83 e 84).

**Ocorrências na mesma mensagem**

- Ocorrências distintas da mesma mensagem são preservadas. A mais grave é destacada, e as secundárias ficam ligadas à mesma fonte (casos 25, 26, 64 e 78).

**Consolidado**

- Agrupado por período e loja e ordenado pela fila da seção 8, com resumo factual, ação, regra citada, situação relatada, pendências e mensagens de origem.
- Ocorrências únicas são contadas separadamente das mensagens. Bloqueios, revisões e erros aparecem em quadros próprios.
- A data de corte é explícita; mensagens sem data ficam fora do filtro temporal e são listadas à parte (caso 87).
- Não inventar fatos, responsáveis, ações executadas nem resolução. O mascaramento da seção 11 vale também para histórico, metadados e arquivos exportados.

**Métricas da consolidação**

| Métrica | Cálculo |
| --- | --- |
| Cobertura de mensagens | Mensagens com destino / mensagens importadas |
| Cobertura de ocorrências | Ocorrências esperadas identificadas / ocorrências esperadas |
| Precisão de ocorrências | Ocorrências previstas corretamente identificadas / ocorrências previstas |
| Precisão de associação | Vínculos corretos / vínculos produzidos |
| Revocação de associação | Vínculos esperados recuperados / vínculos esperados |
| Rastreabilidade | Ocorrências com fontes válidas / ocorrências produzidas |
| Fidelidade do resumo | Afirmações sustentadas nas mensagens / afirmações verificadas |

Zero no denominador significa "não aplicável". Os limiares agregados ainda não foram fixados. O gabarito do lote sintético está em gabarito_consolidacao_lote.json, com o destino de cada mensagem, as ocorrências esperadas, os vínculos, as reincidências e as contagens.

<!-- FIM_CONTEUDO_ORIGINAL -->
