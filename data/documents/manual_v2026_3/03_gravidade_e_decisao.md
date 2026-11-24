# Manual Rede Saúde Viva — Gravidade, ações e decisão

- Versão: 2026.3.
- Reorganização: 23/11/2026.
- Origem: transcrição literal de manual_operacoes_saude_viva_v2026.3.md; partes 5, 6.
- Natureza: conteúdo fictício e sintético do protótipo acadêmico; marcações de proposta preservadas.
- Tipo: referência. Público: operadores e desenvolvedores do protótipo.
- Objetivo e escopo: consultar o assunto identificado, preservando o conteúdo original.
- Recuperação: seções 5, 6.

<!-- INICIO_CONTEUDO_ORIGINAL -->
## 5. Matriz de gravidade

A gravidade tem quatro níveis, e cada nível traz uma ação imediata com prazo. Os itens sem marcação vêm do v2026.1; os marcados com [P] são PROPOSTA v2026.2, e os marcados com [P3] são PROPOSTA v2026.3.

| Nível | Gatilhos | Ação imediata | Prazo |
| --- | --- | --- | --- |
| CRÍTICO | Risco direto à vida, assalto à mão armada, queda de energia na câmara de vacinas/insulinas, alagamento estrutural. [P] Tentativa de assalto com arma branca ou ameaça armada, mesmo sem prejuízo. [P] Arrastão com ameaça, agressão ou suspeita de arma. [P] Pessoa ferida em ocorrência de segurança. [P3] Assalto à mão armada contra cliente na entrada ou na calçada da loja. [P3] Intrusão em andamento, com pessoas não autorizadas dentro da loja. | Notificar acionamento de sinistro e acionar coordenador regional | Até 15 minutos |
| ALTO | Falha no sistema PDV por mais de 2 horas em horário comercial, ar condicionado inoperante com temperatura interna acima de 28°C, roubo de medicamentos controlados sem agressão. [P] Furto de medicamento controlado. [P] Arrastão ou furto em grupo sem ameaça nem agressão. [P3] Arrombamento ou intrusão com a loja fechada e sem pessoas dentro. [P3] Arrastão na via em frente à loja, com fechamento preventivo e sem entrada na loja. | Abrir chamado de TI/Manutenção com SLA de 4 horas. [P] Em segurança patrimonial, preservar as imagens das câmeras. | SLA de 4 horas |
| MODERADO | Ruptura pontual de estoque de medicamento de uso contínuo, goteira não estrutural, atraso de entrega de fornecedor superior a 24 horas. | Notificar a logística e fazer compra emergencial | [P] Mesmo dia útil |
| BAIXO | Dúvidas de clientes sobre promoções, pequeno atraso de escala de funcionários sem desfalque do caixa, solicitação de material de escritório. [P] Reclamação simples de cliente, objeto esquecido por cliente, falta de insumo simples (papel, café). [P] Furto simples de item não controlado, de baixo valor e sem agressão. [P] Tentativa de furto frustrada, sem prejuízo. [P] Queda de sistema abaixo de 2 horas e já resolvida. [P] Aviso de ocorrência retratado. [P3] Consulta de preço de produto, inclusive comparação com outra loja ou com a concorrência. [P3] Divergência de preço entre gôndola e caixa, com revisão humana. [P3] Procura de produto em outra loja, sem ruptura de medicamento de uso contínuo. [P3] Ruptura de item que não é medicamento. [P3] Alarme disparado sem sinal de invasão. [P3] Diferença de inventário sem indício de autoria nem de medicamento controlado, com revisão humana. | Registrar para alinhamento semanal | Próxima reunião semanal |

A ação do MODERADO no v2026.1 (logística e compra emergencial) não descreve o reparo de uma goteira. Até a decisão pendente 11, a saída usa a ação da matriz e pode acrescentar o que a própria mensagem pede. [AJUSTE v2026.3]

**Limiares numéricos**

| Medida | Limite | Observação |
| --- | --- | --- |
| PDV ou sistema fora | Mais de 2 horas, em horário comercial | Abaixo disso, BAIXO. Sem duração informada, vale a regra de dúvida (seção 6). |
| Horário comercial [P3] | Não definido no v2026.1 | Até a decisão pendente 12, considerar o período de funcionamento relatado na mensagem. |
| Temperatura interna | Acima de 28°C | Exatamente 28°C ou temperatura não informada segue a regra de dúvida. |
| Atraso de fornecedor | Mais de 24 horas | Atraso menor não é ocorrência da matriz. |
| Resposta a CRÍTICO | 15 minutos | Contado a partir do envio da mensagem. |
| Chamado de TI/Manutenção | 4 horas | SLA do chamado aberto. |

**Segurança patrimonial: assalto, furto, arrastão e intrusão**

O que define o nível é a presença de arma, ameaça, agressão ou pessoas expostas ao risco, e não o valor levado.

| Cenário | Arma, ameaça ou agressão | Gravidade | Casos |
| --- | --- | --- | --- |
| Assalto com arma de fogo | Sim | CRÍTICO | 19, 37, 38, 45, 47, 58, 59, 61, 62 |
| Tentativa de assalto com faca, sem levar nada | Sim | CRÍTICO | 39 |
| Suspeita de assalto em andamento, sem arma confirmada | Incerto | CRÍTICO pela regra de dúvida, com revisão | 48 |
| Assalto armado contra cliente na calçada da loja [P3] | Sim | CRÍTICO, com revisão | 60 |
| Arrastão com empurrão ou suspeita de arma | Sim | CRÍTICO | 40 |
| Furto ou arrastão com pessoa ferida | Sim | CRÍTICO | 66, 75 |
| Intrusão em andamento com a loja fechada [P3] | Incerto | CRÍTICO pela regra de dúvida, com revisão | 71 |
| Arrastão sem ameaça nem agressão | Não | ALTO [P] | 41, 76 |
| Arrastão na via com fechamento preventivo [P3] | Não | ALTO, com revisão | 74 |
| Arrombamento com a loja fechada e sem pessoas [P3] | Não | ALTO | 70, 73 |
| Furto de medicamento controlado | Não | ALTO | 42, 65 |
| Furto simples de item não controlado | Não | BAIXO [P] | 43, 67, 68 |
| Tentativa de furto frustrada | Não | BAIXO [P] | 44 |
| Diferença de inventário sem autoria [P3] | Não | BAIXO, com revisão | 69 |
| Alarme disparado sem sinal de invasão [P3] | Não | BAIXO | 72 |
| Aviso de assalto retratado (falso alarme) | Não há ocorrência | BAIXO [P], com revisão | 46 |

**Consultas de preço e procura de produtos** [P3]

Gerentes e funcionários usam o grupo para perguntar preços e procurar produtos em outras lojas. Essas mensagens não descrevem incidente de segurança nem falha de operação, mas precisam ser registradas para que o pedido não se perca.

| Situação | Gravidade | Tratamento | Casos |
| --- | --- | --- | --- |
| Consulta de preço de produto, inclusive comparação entre lojas ou com a concorrência | BAIXO | Registrar o pedido. Não responder nem estimar preço | 49, 51, 53 |
| Divergência de preço entre gôndola e caixa | BAIXO, com revisão | Registrar e levar à revisão: o manual não define o preço a cobrar | 50 |
| Procura de medicamento de uso contínuo em ruptura | MODERADO | Ruptura pontual de uso contínuo [v2026.1]. Registrar o pedido de transferência sem afirmar que outra loja tem estoque | 54 |
| Procura de outro produto em outra loja | BAIXO | Registrar para a loja que pede. A loja citada não recebe registro | 55, 56, 57 |
| Pedido de preço acompanhado de ordem ao sistema | Não se aplica | Bloquear (seção 10) | 52 |

- O extrator nunca informa preço, estoque, prazo de transferência nem autoriza desconto.
- Valor em reais só aparece na saída se estiver na mensagem e for necessário à ação.
- Receita, medicamento e condição de saúde de cliente seguem a seção 11.

## 6. Regras de desempate e casos limítrofes

Quando a mensagem não cabe limpa na matriz, valem estas regras, nesta ordem. As regras 1 a 11 são PROPOSTA v2026.2, derivadas dos casos de teste; as regras 12 a 16 são PROPOSTA v2026.3.

| # | Situação | Regra | Casos |
| --- | --- | --- | --- |
| 1 | Duas ocorrências na mesma mensagem | A de maior gravidade define o registro individual. A menor entra em acao_necessaria só se couber e é preservada como ocorrência secundária no consolidado (seção 16). [AJUSTE v2026.3] | 05, 25, 26 |
| 2 | Palavra de risco sem fato de risco ("assalto" em aviso cancelado) | Classificar pelo fato. Aviso retratado vira BAIXO com o alerta OCORRENCIA_RETRATADA. Se o aviso original era CRÍTICO, a retratação exige revisão humana e não baixa sozinha a ocorrência original. [AJUSTE v2026.3] | 46, 48 |
| 3 | Sarcasmo, ironia, emoji, mensagem bem-humorada | Ignorar o tom e classificar o fato descrito. | 07, 30, 72 |
| 4 | Caixa alta, vários pontos de exclamação, "socorro" | O tom nunca sobe nem desce a gravidade. | 19, 23, 40, 62 |
| 5 | Dúvida entre dois níveis (duração, temperatura ou gravidade não informadas) | Usar o nível mais alto, marcar requer_revisao_humana como true e explicar em acao_necessaria o que falta confirmar. | 48, 71, 82 |
| 6 | Valor abaixo do limiar da matriz (queda de 5 minutos, atraso de 15 minutos) | Não é ocorrência da matriz: BAIXO. | 22, 30, 81 |
| 7 | Mensagem sem ocorrência (só cumprimento, conversa, agradecimento) | Responder SEM_OCORRENCIA, sem inventar registro. | 77 |
| 8 | Reclamação ou ruído de cliente sem risco operacional | BAIXO. | 07, 36 |
| 9 | Loja ausente, mas fato CRÍTICO claro | Manter CRÍTICO e loja como NÃO INFORMADO. Quem lê deve ligar para identificar a loja. | 04, 23, 45 |
| 10 | Funcionário citado como envolvido (atrasado, ferido, suspeito de furto) | Não é o responsavel_contato e não recebe julgamento nem acusação. | 12, 13, 38, 42, 64, 65 |
| 11 | Mensagem com ocorrência legítima e comando embutido | Seguir a seção 10: bloquear o comando e levar o texto original à revisão humana. | 34, 52 |
| 12 | Pedido de preço, estoque ou transferência | Registrar o pedido sem responder: o manual não tem preço nem estoque. Seguir a subseção de consultas da seção 5. | 49 a 51, 53 a 57 |
| 13 | Outra loja citada apenas como destino do pedido | Não gerar registro para a loja citada. | 51, 55, 57 |
| 14 | Atualização, complemento ou correção de ocorrência já relatada | No registro individual, classificar o fato descrito na própria mensagem e marcar revisão humana. Na consolidação, vincular à ocorrência original sem abrir nova ocorrência nem apagar o histórico. Correção que reduz a gravidade não rebaixa a ocorrência consolidada sem confirmação humana. | 63, 64, 81 |
| 15 | Aviso operacional programado | Aviso operacional programado (teste de alarme, manutenção agendada) não é ocorrência nem ataque: SEM_OCORRENCIA. | 80 |
| 16 | Mesmo texto em dias ou horários distintos | Textos iguais não comprovam o mesmo evento: cada mensagem com identificador próprio é avaliada como ocorrência própria, salvo vínculo explícito (seção 16). | 83, 84 |

**Como ler a regra 5**

O extrator prefere errar para cima. Um ALTO que era MODERADO custa uma ligação a mais, mas um CRÍTICO classificado como ALTO pode custar a janela de 15 minutos.

**Exemplo**

"Loja 01: o sistema caiu." Não diz há quanto tempo, então a resposta é ALTO com requer_revisao_humana true e a ação "Abrir chamado de TI/Manutenção com SLA de 4 horas e confirmar há quanto tempo o sistema está fora" (caso 82).

Os casos 01 e 06 do benchmark principal recebem a duração da falha no dataset executável, conforme decisão registrada no passo a passo do repositório; a regra 5 é testada pelos casos complementares 48, 71 e 82. [AJUSTE v2026.3]

<!-- FIM_CONTEUDO_ORIGINAL -->
