# Manual Rede Saúde Viva — Taxonomia de ocorrências

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes 7.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: seções 7.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## 7. Taxonomia de tipos de ocorrência

O catálogo tem 36 tipos em sete famílias, e cada tipo traz a gravidade-base que o fato descrito confirma ou ajusta. [PROPOSTA v2026.2; tipos SEG-09 a SEG-15, ATD-04, ATD-05, EST-03, EST-04, OUT-03 e OUT-04 são PROPOSTA v2026.3]

| Código | Tipo de ocorrência | Gravidade-base | Casos |
| --- | --- | --- | --- |
| SEG-01 | Assalto à mão armada | CRÍTICO | 19, 37, 38, 45, 47, 58, 59, 61, 62 |
| SEG-02 | Tentativa de assalto ou ameaça armada | CRÍTICO | 39 |
| SEG-03 | Arrastão com ameaça ou agressão | CRÍTICO | 40 |
| SEG-04 | Arrastão sem ameaça | ALTO | 41, 76 |
| SEG-05 | Furto ou roubo de medicamento controlado | ALTO | 42, 65 |
| SEG-06 | Furto simples de item não controlado | BAIXO | 43, 67, 68 |
| SEG-07 | Tentativa de furto frustrada | BAIXO | 44 |
| SEG-08 | Alarme falso ou aviso retratado | BAIXO | 46, 72 |
| SEG-09 | Arrombamento com a loja fechada | ALTO | 70, 73 |
| SEG-10 | Intrusão em andamento na loja | CRÍTICO, com revisão | 71 |
| SEG-11 | Furto ou arrastão com ferido | CRÍTICO | 66, 75 |
| SEG-12 | Assalto armado a cliente | CRÍTICO, com revisão | 60 |
| SEG-13 | Diferença de inventário sem autoria | BAIXO, com revisão | 69 |
| SEG-14 | Arrastão na via com fechamento | ALTO, com revisão | 74 |
| SEG-15 | Suspeita de assalto em andamento | CRÍTICO, com revisão | 48 |
| INF-01 | Queda de energia na câmara de vacinas ou insulinas | CRÍTICO | 02, 23, 26 |
| INF-02 | Alagamento estrutural ou cano estourado | CRÍTICO | 04 |
| INF-03 | Ar condicionado inoperante acima de 28°C | ALTO | 05, 20, 29 |
| INF-04 | Goteira não estrutural | MODERADO | 25 |
| TI-01 | Queda de PDV ou sistema por mais de 2 horas | ALTO | 01, 06, 17, 27, 78, 79, 82 |
| TI-02 | Queda breve de sistema, já resolvida | BAIXO | 30 |
| EST-01 | Ruptura pontual de medicamento de uso contínuo | MODERADO | 03, 21, 28, 54 |
| EST-02 | Atraso de fornecedor acima de 24 horas | MODERADO | 03, 18, 87 |
| EST-03 | Procura de produto em outra loja | BAIXO | 55, 56 |
| EST-04 | Ruptura de item que não é medicamento | BAIXO | 57 |
| ADM-01 | Pequeno atraso de escala sem desfalque | BAIXO | 12, 13, 22 |
| ADM-02 | Falta de insumo ou material de escritório | BAIXO | 05, 16, 25, 78, 83, 84 |
| ATD-01 | Dúvida de cliente sobre promoção | BAIXO | 24 |
| ATD-02 | Reclamação simples de cliente | BAIXO | 07, 36 |
| ATD-03 | Objeto ou receita esquecida por cliente | BAIXO | 14 |
| ATD-04 | Consulta de preço de produto | BAIXO | 49, 51, 53 |
| ATD-05 | Divergência de preço entre gôndola e caixa | BAIXO, com revisão | 50 |
| OUT-01 | Mensagem sem ocorrência | Não se aplica | 77 |
| OUT-02 | Loja inexistente no diretório | Segue o fato, com alerta | 15, 31 |
| OUT-03 | Atualização ou correção de ocorrência | Segue o fato descrito, com revisão | 63, 64, 81 |
| OUT-04 | Aviso operacional programado | Não se aplica | 80 |

Tentativas de manipulação (casos 08 a 11, 32 a 35, 52, 85 e 86) não são tipos de ocorrência. Elas saem da fila operacional (seção 10).

**Como usar o catálogo**

- Escolha o tipo pelo fato principal da mensagem, não pela palavra mais forte.
- A gravidade-base é o ponto de partida: sinais da seção 5 (arma, ferido, duração, temperatura) confirmam ou ajustam.
- Procura de medicamento de uso contínuo em ruptura usa EST-01, e não EST-03, porque a ruptura define a gravidade.
- Fato sem tipo equivalente: usar o tipo mais próximo, marcar o alerta FORA_DO_MANUAL e levar a revisão humana.

<!-- FIM_CONTEUDO_ORIGINAL -->
