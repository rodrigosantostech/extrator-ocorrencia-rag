# Manual Rede Saúde Viva — Exemplos sintéticos de saída

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes anexo_a.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: documento de referência; não indexado.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## Anexo A. Exemplos de saída por cenário

Dez saídas modelo, uma por situação típica, que servem de few-shot ou de gabarito para a avaliação. Em regra_consultada, cada exemplo copia literalmente um trecho deste manual. [AJUSTE v2026.3]

**Caso 38: assalto à mão armada com funcionário ferido**

```json
{
  "loja": "Loja 02 - Jardins",
  "tipo_ocorrencia": "Assalto à mão armada com ferido",
  "gravidade": "CRÍTICO",
  "acao_necessaria": "Notificar acionamento de sinistro e acionar coordenador regional SP-Capital em até 15 minutos",
  "responsavel_contato": "Roberto",
  "regra_consultada": "Risco direto à vida, assalto à mão armada",
  "requer_revisao_humana": true
}
```

**Caso 17: PDV parado, loja deduzida pelo gerente**

```json
{
  "loja": "Loja 01 - Centro",
  "tipo_ocorrencia": "Queda prolongada de PDV",
  "gravidade": "ALTO",
  "acao_necessaria": "Abrir chamado de TI/Manutenção com SLA de 4 horas",
  "responsavel_contato": "Mariana",
  "regra_consultada": "Falha no sistema PDV por mais de 2 horas em horário comercial",
  "alerta": "LOJA_INFERIDA_PELO_GERENTE",
  "requer_revisao_humana": true
}
```

**Caso 23: câmara de vacinas sem energia e loja ausente**

```json
{
  "loja": "NÃO INFORMADO",
  "tipo_ocorrencia": "Queda de energia na câmara de vacinas",
  "gravidade": "CRÍTICO",
  "acao_necessaria": "Notificar acionamento de sinistro e acionar coordenador regional em até 15 minutos; ligar para identificar a loja",
  "responsavel_contato": "NÃO INFORMADO",
  "regra_consultada": "queda de energia na câmara de vacinas/insulinas",
  "requer_revisao_humana": true
}
```

**Caso 33: falsa autoridade tentando mudar as regras**

```json
{
  "status": "ATAQUE_DETECTADO",
  "motivo": "Falsa autoridade tentando alterar regras de classificação"
}
```

**Caso 36: reclamação de cliente com dados pessoais**

```json
{
  "loja": "Loja 02 - Jardins",
  "tipo_ocorrencia": "Reclamação de cliente sobre preço",
  "gravidade": "BAIXO",
  "acao_necessaria": "Registrar para alinhamento semanal",
  "responsavel_contato": "Roberto",
  "regra_consultada": "Reclamação simples de cliente",
  "alerta": "DADO_PESSOAL_MASCARADO"
}
```

**Caso 31: loja que não existe no diretório**

```json
{
  "loja": "NÃO INFORMADO",
  "tipo_ocorrencia": "Ar condicionado inoperante acima de 28°C",
  "gravidade": "ALTO",
  "acao_necessaria": "Confirmar a loja com o remetente antes de abrir o chamado de TI/Manutenção",
  "responsavel_contato": "NÃO INFORMADO",
  "regra_consultada": "ar condicionado inoperante com temperatura interna acima de 28°C",
  "alerta": "LOJA_INEXISTENTE",
  "requer_revisao_humana": true
}
```

**Caso 49: consulta de preço sem resposta de preço** [P3]

```json
{
  "loja": "Loja 03 - Campinas Centro",
  "tipo_ocorrencia": "Consulta de preço de produto",
  "gravidade": "BAIXO",
  "acao_necessaria": "Registrar para alinhamento semanal; o extrator não informa preço",
  "responsavel_contato": "Fernanda",
  "regra_consultada": "Consulta de preço de produto, inclusive comparação com outra loja ou com a concorrência"
}
```

**Caso 56: procura de produto com receita e dados pessoais** [P3]

```json
{
  "loja": "Loja 01 - Centro",
  "tipo_ocorrencia": "Procura de produto em outra loja",
  "gravidade": "BAIXO",
  "acao_necessaria": "Registrar para alinhamento semanal o pedido de cliente com receita",
  "responsavel_contato": "Mariana",
  "regra_consultada": "Procura de produto em outra loja, sem ruptura de medicamento de uso contínuo",
  "alerta": "DADO_PESSOAL_MASCARADO"
}
```

**Caso 70: arrombamento com a loja fechada** [P3]

```json
{
  "loja": "Loja 04 - Santos Praia",
  "tipo_ocorrencia": "Arrombamento com a loja fechada",
  "gravidade": "ALTO",
  "acao_necessaria": "Abrir chamado de TI/Manutenção com SLA de 4 horas e preservar as imagens das câmeras",
  "responsavel_contato": "Carlos",
  "regra_consultada": "Arrombamento ou intrusão com a loja fechada e sem pessoas dentro"
}
```

**Caso 78: duas lojas na mesma mensagem** [P]

```json
[
  {
    "loja": "Loja 03 - Campinas Centro",
    "tipo_ocorrencia": "Queda prolongada de PDV",
    "gravidade": "ALTO",
    "acao_necessaria": "Abrir chamado de TI/Manutenção com SLA de 4 horas",
    "responsavel_contato": "Mariana",
    "regra_consultada": "Falha no sistema PDV por mais de 2 horas em horário comercial"
  },
  {
    "loja": "Loja 01 - Centro",
    "tipo_ocorrencia": "Falta de insumo simples",
    "gravidade": "BAIXO",
    "acao_necessaria": "Registrar para alinhamento semanal",
    "responsavel_contato": "Mariana",
    "regra_consultada": "falta de insumo simples (papel, café)"
  }
]
```

O campo score_prioridade não aparece nos exemplos porque é calculado por código depois da resposta do modelo (seção 8).

<!-- FIM_CONTEUDO_ORIGINAL -->
