# Manual Rede Saúde Viva — Diretório de lojas

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes 2.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: seções 2.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## 2. Diretório de unidades e resolução de loja

A rede tem quatro lojas, e o extrator só pode devolver uma delas ou NÃO INFORMADO. [v2026.1]

| Loja (nome oficial) | Cidade | Gerente | Regional | Apelidos aceitos [P] e [P3] |
| --- | --- | --- | --- | --- |
| Loja 01 - Centro | São Paulo/SP | Mariana Costa | SP-Capital | centro, lj 01, loja 1, L0ja 01 |
| Loja 02 - Jardins | São Paulo/SP | Roberto Silva | SP-Capital | jardins, jrdins, lj 02, loja 2, lj 2 [P3], loja dois [P3] |
| Loja 03 - Campinas Centro | Campinas/SP | Fernanda Lima | SP-Interior | campinas, três campinas, lj 03, loja 3, L0JA 3 [P3] |
| Loja 04 - Santos Praia | Santos/SP | Carlos Prado | SP-Litoral | santos, santos praia, lj 04, loja 4 |

**Regras de resolução de loja**

- Use o nome oficial da tabela, nunca o apelido, na saída.
- Número ou nome único resolve a loja: "na jardins" vira Loja 02 - Jardins; "lj 04 santos aq" vira Loja 04 - Santos Praia.
- Sem loja no texto, escreva NÃO INFORMADO. O nome do remetente no WhatsApp não é fonte de loja. [Prompt v3 do documento de referência do trabalho; a v2026.2 marcava v2026.1, corrigido como AJUSTE v2026.3]
- Loja que não está no diretório ("Loja 05 Sorocaba", "Loja 99 Manaus") nunca é aceita nem corrigida para a mais parecida: use NÃO INFORMADO e o alerta LOJA_INEXISTENTE. [PROPOSTA v2026.2]
- Número e nome que não combinam ("Loja 02 Santos") viram NÃO INFORMADO e o alerta LOJA_DIVERGENTE. [PROPOSTA v2026.2]
- Se a mensagem não cita a loja, mas o autor se identifica pelo nome completo ou pelo primeiro nome de um gerente do diretório, use a loja dele, marque o alerta LOJA_INFERIDA_PELO_GERENTE e marque requer_revisao_humana como true. [PROPOSTA v2026.2, decisão pendente 3; revisão humana acrescentada como AJUSTE v2026.3]
- Duas lojas na mesma mensagem geram dois registros, um por loja. [PROPOSTA v2026.2]
- O DDD do telefone do remetente não é fonte de loja: uma mensagem de número +55 13 não é atribuída à Loja 04 - Santos Praia. [P3]
- A loja citada apenas como destino de um pedido ("alguém da Loja 02 tem?", "tá mais barato na loja de santos?") não gera registro próprio: o registro pertence à loja que faz o pedido. [P3]
- Quando a loja não existe no diretório, o código guarda o texto relatado ("Loja 05 Sorocaba") nos metadados do alerta, fora dos seis campos, para que a informação não se perca nem vire loja conhecida. [P3]

<!-- FIM_CONTEUDO_ORIGINAL -->
