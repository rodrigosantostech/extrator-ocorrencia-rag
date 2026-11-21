# Extrator de Ocorrências com RAG

Projeto acadêmico de extração e triagem de mensagens operacionais da empresa fictícia **Rede Saúde Viva**, com comparação de prompts v1, v2 e v3, consulta ao manual operacional e avaliação de segurança.

A implementação planejada usa **Python local no Windows e GPT pela API da OpenAI**.

## Documentação

- [Requisitos oficiais do MBA](docs/TRABALHO_MBA.md): consolidação das exigências R1–R5 e dos entregáveis E1–E4.

- [Referência aproximada da solução pretendida](docs/Trabalho_Final_MBA_Extrator_Ocorrencias.md): guia do que queremos construir, com problema, prompts, manual, 16 casos e ideias para relatório e pitch. Os detalhes serão adaptados às decisões do projeto e às exigências do professor.
- [Passo a passo de execução](docs/PASSO_A_PASSO.md): tarefas, dependências, critérios de conclusão e cronograma adaptados às decisões do projeto.

## Objetivo operacional confirmado

**21/11/2026 — origem: esclarecimento do usuário nesta conversa.** Apoiar a área que acompanha ocorrências em lojas, como assaltos e outros incidentes, recebidas em mensagens textuais pelo WhatsApp. Processar o conjunto de mensagens e consolidar ocorrências por loja e prioridade, relacionando relatos e atualizações com fontes rastreáveis.

Fluxo planejado: lote de mensagens → mascaramento e triagem → extração e consulta ao manual → validação → associação de relatos e atualizações → consolidado → revisão humana.

O RAG fornece as regras de classificação e ação. A consolidação relaciona as mensagens e preserva ocorrências distintas. O protótipo deve validar lotes sintéticos por arquivo; a conexão automática ao WhatsApp permanece uma evolução proposta, sem conector implementado ou definido. Áudios e imagens ficam fora do recorte textual.

## Base de conhecimento

- [Manual de operações da Rede Saúde Viva](data/documents/manual_operacoes_saude_viva.md): primeiro documento da base, versão 2026.1, com cadastro de lojas, classificação de ocorrências e privacidade. Convertido do arquivo fornecido pelo usuário, preservando o conteúdo operacional.

## Estado atual

A documentação e o primeiro manual da base de conhecimento foram preparados. O protótipo, a integração com a API, o dataset executável e o benchmark ainda serão implementados seguindo o passo a passo.

Conforme esclarecimento do usuário em 21/11/2026, o documento convertido representa, em linhas gerais, o que queremos fazer; orienta a solução sem fixar todos os detalhes. Suas referências a Gemini/Colab ficam como histórico, pois a implementação planejada usa Python no Windows e API da OpenAI. Percentuais, proteções e status declarados no Word continuam sem comprovação neste repositório.

## Próximas entregas

1. Revisar os requisitos e as divergências entre manual e casos esperados.
2. Preparar Python, acesso à API e os 16 casos de teste.
3. Implementar e comparar v1/v2 para o checkpoint de **23/11/2026**.
4. Implementar recuperação, v3, validações, consolidação em lote e avaliações separadas de extração e consolidação.
5. Finalizar relatório de até oito páginas e pitch de sete minutos para **25/11/2026**.

Os comandos de instalação, execução e teste do aplicativo serão documentados quando o protótipo estiver implementado.
