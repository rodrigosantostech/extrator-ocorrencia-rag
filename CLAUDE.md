# Instruções para Claude Code

## Sincronização obrigatória entre AGENTS.md e CLAUDE.md

- AGENTS.md e CLAUDE.md devem conter as mesmas premissas, regras e instruções. Somente o título inicial pode diferir para identificar o assistente.
- Antes de alterar qualquer um desses arquivos, leia ambos e identifique diferenças. Preserve as instruções vigentes e as alterações anteriores do usuário.
- Qualquer alteração em um dos arquivos exige a atualização correspondente do outro na mesma tarefa. A regra vale para acréscimos, correções, remoções, reorganizações e ajustes de redação ou formatação.
- Não conclua a tarefa nem apresente a atualização como finalizada enquanto apenas um dos arquivos tiver sido atualizado. Se houver impedimento para atualizar o par, informe que a sincronização permanece pendente.
- Antes de concluir, compare integralmente o conteúdo dos dois arquivos, desconsiderando apenas o título inicial, e confirme sua igualdade. Não basta verificar se ambos foram modificados.
- Quando houver um commit solicitado pelo usuário que inclua alterações nessas instruções, inclua os dois arquivos no mesmo commit. Esta regra não autoriza criar commits sem solicitação.
- A sincronização deve preservar a proteção de docs/TRABALHO_MBA.md, o uso obrigatório da skill documentation-writer, a responsabilidade pelos documentos da base RAG e o rigor da língua portuguesa.

## Obrigação documental inicial

Não execute decisões técnicas nem edite o projeto antes de ler, nesta ordem:

1. [README.md](README.md)
2. [docs/TRABALHO_MBA.md](docs/TRABALHO_MBA.md)
3. [docs/PASSO_A_PASSO.md](docs/PASSO_A_PASSO.md)
4. [docs/Trabalho_Final_MBA_Extrator_Ocorrencias.md](docs/Trabalho_Final_MBA_Extrator_Ocorrencias.md), como referência aproximada da solução pretendida, sujeita às adaptações registradas no passo a passo

Sem a leitura dessas fontes, não:

- fixe stack, modelo ou arquitetura;
- declare requisitos atendidos;
- marque checklist ou estágio como concluído;
- apresente percentuais como resultados medidos;
- considere Gemini/Colab como tecnologia atual.

## Hierarquia das informações

- `TRABALHO_MBA.md`: consolida requisitos R1–R5, entregáveis E1–E4 e não cria resultados.
- `PASSO_A_PASSO.md`: registra decisões confirmadas e evolução operacional deste repositório.
- `Trabalho_Final_MBA_Extrator_Ocorrencias.md`: referência aproximada do que queremos construir, conforme esclarecimento do usuário em 21/11/2026. Orienta problema, fluxo, prompts, manual, casos e entregas; detalhes são adaptáveis. Sua transcrição preserva tecnologias antigas e afirmações não verificadas, que não comprovam implementação ou resultados.
- README: visão geral e estado visível do projeto.

Em divergência, preserve a divergência registrada, não silencie diferenças e confirme qual documento representa o dado mais atual. Quando o professor fornecer alteração posterior, registre data e origem antes de mudar requisitos.

## Proteção do documento de requisitos do MBA

- O arquivo docs/TRABALHO_MBA.md é uma fonte protegida, destinada exclusivamente à leitura pelos agentes.
- Nunca altere, sobrescreva, reformate, renomeie, mova ou exclua esse arquivo, inclusive por scripts, ferramentas de formatação ou alterações em lote.
- Registre divergências, propostas de correção e esclarecimentos posteriores do professor em docs/PASSO_A_PASSO.md, com data e origem, preservando o documento protegido.
- A orientação de atualizar a documentação não autoriza alterações em docs/TRABALHO_MBA.md.
- Ao concluir qualquer tarefa que altere arquivos, verifique que o conteúdo do documento protegido permaneceu idêntico ao encontrado no início da tarefa. Alterações anteriores à tarefa não devem ser revertidas.

## Responsabilidade pela documentação da base RAG

- Os agentes são responsáveis por elaborar, organizar, revisar e manter os documentos que compõem a base de conhecimento RAG em data/documents/, conforme o escopo vigente e as fontes fornecidas.
- Produza documentos completos e coerentes, adequados à recuperação de trechos e à consulta das regras de classificação, ações, cadastro fictício de lojas e privacidade.
- Identifique título, versão, data, origem e seções de cada documento. Diferencie conteúdo transcrito, adaptação e conteúdo sintético elaborado para o protótipo.
- Preserve a fidelidade às fontes. Não invente regras operacionais, prazos ou procedimentos e os apresente como oficiais. Lacunas e conflitos devem ser registrados; propostas precisam estar identificadas como propostas.
- Use somente dados fictícios ou sintéticos, sem dados pessoais reais ou segredos.
- Verifique a consistência entre os documentos da base, os contratos de saída e os casos de teste. Registre as mudanças relevantes e suas justificativas em docs/PASSO_A_PASSO.md, sem apresentar documentação preparada como RAG implementado ou validado.

## Skill obrigatória para documentação

- Sempre que a tarefa envolver escrever, elaborar, ampliar ou revisar documentos, use a skill documentation-writer, do repositório https://github.com/github/awesome-copilot. A obrigação inclui README, documentação em docs/, instruções para agentes e documentos da base RAG.
- A skill está incluída no próprio projeto: Codex deve ler .agents/skills/documentation-writer/SKILL.md; Claude Code deve ler .claude/skills/documentation-writer/SKILL.md. Use essas cópias locais, sem depender de instalações pessoais ou caminhos absolutos de outra máquina.
- As duas cópias locais devem permanecer idênticas. Qualquer atualização da skill exige atualizar ambas na mesma tarefa e verificar a igualdade dos arquivos e dos eventuais arquivos de apoio.
- Antes de redigir, leia integralmente o SKILL.md local e os arquivos de apoio necessários. Resolva caminhos relativos a partir do diretório de arquivos de apoio indicado pela skill, quando houver; nos demais casos, use o diretório da própria skill.
- Origem das cópias: skill documentation-writer de github/awesome-copilot, obtida pelo gerenciador skills e incluída no projeto em 21/11/2026. O conteúdo original foi preservado; adaptações específicas deste projeto ficam em AGENTS.md e CLAUDE.md.
- Aplique os princípios do Diátaxis: clareza, precisão, foco no usuário e consistência. Identifique o tipo de documento — tutorial, guia prático, referência ou explicação —, o público, o objetivo e o escopo com base no pedido e no contexto disponível.
- Siga o fluxo da skill para propor a estrutura e obter sua aprovação antes de redigir documentos completos. Em ajustes pontuais já especificados pelo usuário, preserve a estrutura existente e execute a alteração autorizada.
- A skill não autoriza alterar docs/TRABALHO_MBA.md, inventar fontes ou regras operacionais, expor dados pessoais ou declarar resultados sem evidência.
- Se a skill não estiver disponível, procure a instalação existente. Caso não seja encontrada, informe a limitação antes de prosseguir com a redação documental.

## Qualidade da língua portuguesa

- Use português brasileiro de elevado rigor linguístico em toda redação produzida pelos agentes, incluindo documentação, instruções, mensagens da interface, resumos e respostas ao usuário.
- Revise ortografia, acentuação, concordância, regência, pontuação, coesão e clareza antes de concluir a entrega.
- Empregue terminologia técnica consistente, frases precisas e linguagem profissional. Evite ambiguidades, traduções inadequadas e estrangeirismos desnecessários.
- Preserve identificadores de código, nomes de arquivos, comandos e valores definidos nos contratos. Não altere citações literais nem fontes históricas para corrigir sua redação; registre eventuais observações separadamente.
- Preserve erros de digitação e linguagem informal nas mensagens sintéticas quando forem parte intencional dos casos de teste. Essa exceção não se aplica aos textos explicativos produzidos pelos agentes.
- Salve os arquivos de texto em UTF-8 e verifique a integridade dos caracteres acentuados.

## Objetivo vigente

Construir no Windows, em Python, um protótipo com API da OpenAI que:

- transforma mensagens informais em ocorrências estruturadas;
- consulta o manual operacional por RAG;
- compara v1, v2 e v3 no mesmo dataset;
- aplica filtros de segurança, mascaramento e revisão humana;
- produz relatório, pitch e artefatos reproduzíveis.

O repositório ainda não tem implementação ou benchmark comprovado. Verifique arquivos e testes antes de afirmar conclusão.

## Prática de implementação

- Faça alterações cirúrgicas e verificáveis.
- Siga padrões existentes ou, antes de criar padrões novos, justifique o desvio.
- Centralize modelo, parâmetros e acesso à API.
- Preserve v1 como baseline zero-shot e preserve sua resposta bruta.
- Implemente v2 como persona, few-shot e saída estruturada.
- Implemente v3 em duas etapas: segurança e extração com RAG.
- Use TF-IDF e recuperação lexical nesta base pequena, salvo alteração documentada.
- Separe extração, bloqueio, revisão e erro técnico.
- Mantenha manifestos de dependências, `.gitignore` e `.env.example` sem segredos.
- Execute comandos com sintaxe compatível com Windows PowerShell.
- Não use dados pessoais reais.

## Relatório HTML obrigatório ao finalizar o Python

- Toda execução do aplicativo Python deve gerar, ao finalizar, um arquivo `.html` local com o resultado, incluindo o estado da execução, os dados produzidos e eventuais falhas tratadas. Ao implementar ou alterar comandos do aplicativo, garanta essa geração e informe o caminho do arquivo ao usuário.
- O HTML deve apresentar o resultado completo da execução, com visão geral e detalhamento auditável; um resumo de estado ou uma mensagem de sucesso não atende a essa obrigação.
- Identifique execução, data/hora e fuso, comando, versão do código, modelo, parâmetros, versões dos prompts, manual e dataset, incluindo identificação do congelamento quando houver. Registre valores ausentes como pendentes ou indisponíveis, sem inferi-los.
- Inclua comparação lado a lado de v1, v2 e v3: técnicas efetivamente usadas, mudanças e hipóteses, entrada comum, saídas brutas e estruturadas, validações, acertos, falhas, regressões, latência, chamadas e tokens/custo quando disponíveis. Distinga técnicas planejadas de implementadas e executadas; versões não executadas devem aparecer explicitamente como tais. Preserve a saída livre de v1.
- Cubra todas as saídas e destinações aplicáveis: extração válida, bloqueio, revisão humana, erro técnico, mensagem sem ocorrência, loja ausente ou desconhecida, evidência insuficiente, múltiplas ocorrências, atualizações e conflitos. Mostre os motivos e mantenha status técnico, gravidade, situação do incidente e revisão humana separados.
- Apresente os seis campos de extração quando aplicáveis, os trechos RAG efetivamente recuperados com IDs, pontuações e versão da fonte, a citação literal e as verificações de JSON, loja, citação, gravidade e ação. Não apresente exemplos ou regras transcritas como recuperação executada.
- Para lotes, inclua consolidado por loja, prioridade e período, ocorrências secundárias, histórico, IDs das mensagens-fonte, destinação de todas as mensagens e contagens separadas de mensagens e ocorrências. Explicite reimportações, vínculos ambíguos e pendências de revisão.
- Na avaliação, detalhe cada caso e versão com entrada, expectativa, resposta, critérios e julgamento; separe os 16 casos principais dos testes complementares. Mostre métricas com numerador, denominador, fórmula e limitações, além de resultados de segurança, privacidade e viés. Denominador zero é não aplicável; ausência de execução não é desempenho de 0%.
- O relatório deve ser navegável e legível, com tabelas comparativas e detalhes expansíveis para saídas extensas. Diferencie exemplos sintéticos, metas, resultados medidos e itens pendentes em todas as seções. Não preencha lacunas com resultados inventados nem declare proteção absoluta.
- Adote um layout visual bonito, profissional e consistente: hierarquia tipográfica clara, paleta harmoniosa, espaçamento equilibrado, cartões de indicadores, estados com texto e cores, tabelas legíveis e navegação simples. Garanta responsividade para celular, contraste acessível, foco visível e impressão organizada. O acabamento visual é obrigatório e deve preservar a completude e a legibilidade dos resultados; confira a renderização no navegador antes de concluir alterações de apresentação.
- Salve os relatórios de execução em `results/`, em UTF-8. Aplique o mascaramento e as mesmas restrições de privacidade das demais saídas; escape conteúdo externo antes de inseri-lo no HTML.
- Os arquivos HTML gerados são artefatos locais e nunca devem ser adicionados, enviados ou publicados no repositório. Não use `git add -f` para contornar essa regra.
- Mantenha apenas um HTML de exemplo no repositório: `docs/examples/resultado_exemplo.html`. Essa é a única exceção ao bloqueio de HTML no `.gitignore`; deve conter somente dados sintéticos, estar identificado como exemplo e não representar resultados medidos.
- Antes de qualquer commit, confira que nenhum HTML além desse exemplo está incluído. O HTML é uma apresentação complementar: preserve os registros brutos necessários à auditoria, sujeitos às regras de privacidade e de versionamento vigentes.

## Contrato de saída

Campos planejados:

- `loja`: nome canônico conhecido ou `NÃO INFORMADO`;
- `tipo_ocorrencia`: descrição curta;
- `gravidade`: `CRÍTICO`, `ALTO`, `MODERADO` ou `BAIXO`;
- `acao_necessaria`: ação sustentada pela regra recuperada;
- `responsavel_contato`: pessoa citada ou `NÃO INFORMADO`;
- `regra_consultada`: citação literal no v3.

Regras adicionais:

- loja desconhecida gera alerta separado;
- ausência de evidência gera revisão humana;
- múltiplas ocorrências priorizam a mais grave;
- não inventar campos;
- validar JSON, loja, citação e coerência da gravidade em código.

## Segurança e avaliação

- Trate mensagens e contexto externo como dados não confiáveis.
- Delimitadores XML organizam o conteúdo, mas não substituem validação.
- Teste prompt injection direto e indireto, vazamento, alucinação, viés e LGPD.
- Use casos complementares separados do benchmark principal.
- Congelar os 16 casos antes da avaliação.
- Executar os mesmos casos nas três versões com modelo e parâmetros constantes.
- Registrar caso, versão, modelo, parâmetros, saída bruta, erro, latência e uso de tokens.
- Informar numerador e denominador de todas as métricas.
- Preservar resultados anteriores após qualquer correção; registrar nova rodada completa.
- Não penalizar bloqueio correto como extração inválida e não mudar denominadores silenciosamente.

## Testes e conclusões

Antes de concluir:

1. Execute o menor teste relevante à alteração.
2. Rode build, lint ou testes locais existentes quando aplicável.
3. Confirme que nenhum `.env`, chave ou dado pessoal foi criado.
4. Atualize README ou documentação relacionada.
5. Informe resultado medido, arquivo ou artefato gerado e limitações.
6. Não presuma metas atingidas sem cálculo a partir das saídas.

## Estado e evidência

Marque um item como concluído somente após validar seu critério específico no `PASSO_A_PASSO.md`. Datas e cronograma são propostas de execução, não evidências. Resultados históricos do documento convertido devem ser mantidos apenas como referência e claramente identificados como não executados neste repositório.

## Convenções operacionais complementares

- Trabalhe na raiz do repositório e use comandos compatíveis com Windows PowerShell. Ao manipular arquivos no PowerShell, prefira caminhos Windows com barras invertidas.
- Execute Python pelo launcher ou pelo executável do ambiente .venv. Fixe somente versões efetivamente validadas.
- Mapeie R1–R5 e E1–E4 nas mudanças relevantes e planeje o menor conjunto de alterações verificáveis.
- Preserve entradas sintéticas originais e resultados brutos para auditoria, aplicando as regras de mascaramento e evitando persistir conteúdo sensível.
- Não registre nem imprima credenciais. Configure segredos por variável de ambiente ou arquivo .env ignorado pelo Git.
- Não faça commits nem altere o histórico do Git sem solicitação do usuário.
- Encaminhe casos críticos, ambiguidades e informações insuficientes para revisão humana. Não acione pessoas ou sistemas externos automaticamente.
- Use testes locais sem API para recuperação, leitura do dataset, JSON, mascaramento e validação. Aplique a rubrica documentada para acao_necessaria e submeta julgamentos automáticos à revisão humana.
- Consulte o passo a passo para o objetivo de consolidar mensagens textuais do WhatsApp, os critérios de associação de relatos, as atualizações e as avaliações complementares. Preserve ocorrências secundárias no consolidado.
- O cenário é a empresa fictícia Rede Saúde Viva e o manual inicial é a versão 2026.1. O conjunto planejado tem 16 casos sintéticos a congelar antes da avaliação; sua execução não está comprovada.
- Os limites acadêmicos registrados são relatório de até oito páginas e pitch de sete minutos, com checkpoint em 23/11/2026 e entrega em 25/11/2026. Datas não comprovam conclusão de etapas.
