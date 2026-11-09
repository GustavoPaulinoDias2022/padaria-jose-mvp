# Fichas de desempenho, portabilidade e impacto

**Formulários em branco; não representam testes ou impacto comprovados.** Preencher somente com medições reais da aplicação implementada. Não misturar tempos de navegação simulada das imagens com carregamento do software.

## Rodada RNF03 — condições controladas

- Data/horário e versão/commit: pendente
- Dispositivo, CPU, RAM, tela e sistema: pendente
- Navegador e versão: pendente
- Servidor, região, plano e versões de runtime/banco: pendente
- Base: confirmar 500 produtos e 5.000 vendas; registrar versão dos dados fictícios
- Página: estoque, primeira página, 25 produtos
- Rede: confirmar limitação de 1,5 Mbps down, 750 kbps up e 150 ms de latência
- Cache do navegador: desativado
- Sessão: autenticada, mesmo perfil e caminho de navegação
- Aquecimento: uma execução antes das cinco medições; registrar resultado separadamente
- Ferramenta: Network/Performance do Chrome DevTools; medir até resultados visíveis e página utilizável
- Interferências, suspensão ou cold start: pendente

| Execução | Tempo até utilização (s) | Condição válida? | Observação/evidência sanitizada |
|---|---|---|---|
| Aquecimento — fora da mediana | — | — | — |
| 1 | — | — | — |
| 2 | — | — | — |
| 3 | — | — | — |
| 4 | — | — | — |
| 5 | — | — | — |

Ordenar os cinco tempos válidos e selecionar o terceiro: essa é a mediana. Aprovar se a mediana for ≤3 segundos. Se houver interferência relevante, documentar e repetir a rodada, sem excluir apenas resultados lentos para melhorar artificialmente a média/mediana. Preservar resultados anteriores e condições.

Cold start: registrar em rodada separada, pois não é comparável à medição aquecida. Se a rede real da padaria for pior que a prevista, executar avaliação adicional e rever a adequação do requisito.

## Portabilidade

| Ambiente | Commit/dependências | Instalação e migrações | Estáticos/login/estoque/venda | Resultado e pendências |
|---|---|---|---|---|
| Windows local | — | — | — | Não executado |
| Linux local | — | — | — | Não executado |
| Linux hospedado | — | — | — | Não executado |
| Navegador/aparelho da parceira | — | Não aplicável ao cliente web | — | Não executado |

Usar instruções versionadas e variáveis de ambiente sem expor valores secretos. Registrar falhas de runtime, dependências, conexão, migrações ou estáticos e corrigir antes de repetir. A ficha não constitui documentação de instalação de um código ainda inexistente.

## Impacto operacional — tempo médio

Comparar vendas fictícias de complexidade equivalente, registrando número de itens e tipo de unidade. Não duplicar vendas reais para medir o sistema. A medição é do registro de uma venda, sem incluir recebimento/pagamento fora do escopo.

| Amostra | Tempo manual (s) | Tempo no sistema (s) | Complexidade/observações |
|---|---|---|---|
| 1 | — | — | — |
| 2 | — | — | — |
| 3 | — | — | — |
| 4 | — | — | — |
| 5 | — | — | — |
| 6 | — | — | — |
| 7 | — | — | — |
| 8 | — | — | — |
| 9 | — | — | — |
| 10 | — | — | — |

Calcular a média de cada método. Redução (%) = (média manual − média sistema) / média manual ×100; exigir média manual maior que zero. Meta proposta: ≥20%. Observar efeito de aprendizagem e interrupções; a amostra pequena não permite generalizar para outros comércios.

## Impacto social — autonomia digital

- Orientação inicial, duração e conteúdo: pendente
- Início/fim de duas semanas de uso: pendente; compatibilizar com cronograma
- Confiança antes e depois: escala 1 (nada confiante) a 5 (muito confiante), pergunta idêntica nos dois momentos: “Quão confiante você se sente para usar o sistema sem ajuda?”

| Tarefa no sistema implementado | Sem ajuda / com ajuda / não concluída | Observação |
|---|---|---|
| Cadastrar produto | — | — |
| Registrar venda | — | — |
| Consultar estoque | — | — |

Meta: três tarefas sem auxílio e confiança final ≥4. A ficha avalia uso do sistema real e difere do teste de três telas. Opinião e comportamento devem ser registrados separadamente. Não divulgar nome ou consentimento no repositório.

## Qualidade do controle — divergência de estoque

Conferir os mesmos dez produtos físicos e comparar ao registro utilizado em cada período: controle manual antes, sistema depois de duas semanas. Registrar códigos anônimos dos itens e quantidades, sem informações comerciais confidenciais em evidência pública.

| Período | Produtos conferidos | Produtos com divergência | Taxa | Observações |
|---|---|---|---|---|
| Antes | 10 | — | — | — |
| Após duas semanas | 10 | — | — | — |

Taxa = produtos divergentes / produtos conferidos ×100. Com dez itens, cada item equivale a dez pontos percentuais. Comparar taxas sem afirmar causalidade exclusiva do software: reposição, perdas e disciplina de registro também influenciam.

## Decisão e revisão

Registrar resultado, limitações, ações e data do reteste. Desempenho insuficiente exige examinar consultas, índices, paginação, recursos estáticos e infraestrutura. Baixa autonomia exige rever linguagem e interação. Divergências exigem verificar o fluxo, o modelo e a rotina de registro. Não atribuir falhas ao participante.
