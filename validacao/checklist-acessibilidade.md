# Verificação de acessibilidade das três telas — RNF04

**Situação: planejado, sem testes executados.** As imagens permitem observar organização e mensagens, mas não comprovam dimensões em pixels CSS, semântica, teclado ou comportamento responsivo da aplicação.

## Identificação da avaliação

- Versão/commit e tipo de artefato (imagem, protótipo interativo ou aplicação): pendente
- Data, responsável e ambiente: pendente
- Dispositivo, tela, sistema, navegador e ampliação: pendente
- Tecnologia assistiva e versão, quando utilizada: pendente

## Checklist por propriedade

| ID | Tela/componentes | Procedimento | Critério de aprovação | Estado |
|---|---|---|---|---|
| ACE01 | Menu, Nova venda e resultado; botões e links de ação | Medir a área acionável no navegador, não a dimensão de um PNG | Ações com alvo mínimo de 44 × 44 pixels CSS | Não executado |
| ACE02 | Títulos, rótulos, valores, botões e mensagens | Medir pares de cores nos estados normal, foco e erro | Texto com contraste ≥4,5:1; bordas/indicadores necessários para identificar controles com ≥3:1 | Não executado |
| ACE03 | Três telas | Ampliar a 200% e executar as tarefas | Nenhum conteúdo ou controle essencial oculto, sobreposto ou inacessível | Não executado |
| ACE04 | Menu e formulário de venda | Navegar por Tab/Shift+Tab e ativar ações por teclado | Ordem lógica, foco visível, nenhuma armadilha e mesmas ações essenciais disponíveis | Não executado |
| ACE05 | Produto e Quantidade | Inspecionar associação de label e campo e verificar o nome acessível | Rótulo persistente e associado programaticamente; unidade compreensível sem depender do placeholder | Não executado |
| ACE06 | Mensagens de validação do formulário | Enviar quantidade inválida e tentar corrigir por teclado | Campo problemático identificado; mensagem explica a correção e é associada ao campo; dados válidos preservados | Não executado |
| ACE07 | Resultado de sucesso e alertas previstos | Avaliar compreensão sem usar a cor como única pista | Texto e símbolo identificam estado e próximo passo; mensagem de rede não afirma sucesso | Não executado |
| ACE08 | Resultado e mensagens dinâmicas | Executar o fluxo com leitor de tela, sem cliques do avaliador | Mensagem anunciada e contexto do foco compreensível, sem anúncio duplicado desnecessário | Não executado |
| ACE09 | Três telas no aparelho da parceira | Confirmar dispositivo e testar orientação/tamanho disponíveis | Seleção de produto, quantidade, total e continuidade utilizáveis sem perda de informação | Não executado |

44 × 44 pixels CSS é o limite adotado pelo projeto. Não se declara conformidade integral com WCAG apenas por preencher este checklist.

## Estados que exigem preparação adicional

As capturas atuais mostram menu, venda pronta para confirmar e sucesso. Antes de verificar ACE06 e os alertas de ACE07, preparar estados interativos de quantidade inválida, estoque insuficiente, sessão expirada e conexão interrompida. Não registrar esses estados como testados usando somente a imagem de sucesso.

## Validação externa e decisão

A proprietária realizará as três tarefas descritas no [plano de validação](../docs/08-validacao.md). Registrar o que consegue ler, localizar, interpretar e corrigir, separando observação de opinião. Não presumir deficiência, nem inferir acessibilidade universal a partir de uma única participante.

Uma barreira que impeça a tarefa central ou o reconhecimento do resultado exige correção e novo teste. Detalhes visuais sem impacto funcional podem ser priorizados para a iteração seguinte, desde que os critérios mínimos sejam atendidos. Testes automatizados poderão auxiliar, mas não substituem teclado, ampliação, tecnologia assistiva e avaliação de compreensão.

## Registro de achado

| ID da verificação | Comportamento observado | Impacto/barreira | Evidência sanitizada | Correção/commit | Reteste |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

Preservar apenas dados autorizados e necessários. Identificação completa e consentimento da participante permanecem fora do repositório público.
