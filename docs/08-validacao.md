# Plano de validação externa

## Participação e data

Representante: proprietária da Padaria José, usuária direta e conhecedora da rotina. Nome completo omitido nesta versão pública. Concordância será obtida antes do teste por declaração ou mensagem após explicação de objetivo, tarefas e uso do feedback. Fotos/áudios exigem autorização específica. Consentimentos e registros identificáveis permanecerão privados.

Data planejada: **20/11/2026**, em horário de menor movimento, a combinar. Não há comprovação de teste realizado. Atualizar a data se o cronograma mudar.

## Método

Teste presencial de 20–30 minutos, protótipo v1 com três imagens e dados fictícios. Confirmar aparelho real, tela, navegador, zoom e conexão. O formato inicial pode exigir visualizar as imagens com zoom; registrar qualquer adaptação que afete a avaliação.

Explicar que a interface está sendo avaliada, não a pessoa. Ler uma tarefa por vez, sem sugerir botões. A participante aponta ou descreve as ações; o avaliador troca a imagem. Isso avalia compreensão e navegação simulada, não funcionalidade, persistência ou desempenho.

Releitura permitida. Orientação sobre campo, controle ou caminho é ajuda e deve ser registrada. Observar escolhas, hesitações, interpretações e pedidos de auxílio, separadamente de opiniões. Encerrar com escala neutra e comentários livres. Gravar ou fotografar apenas se autorizado.

## Exatamente três tarefas

| Tarefa | Objetivo apresentado | Estado/dados | Resultado esperado | Registrar | Requisitos |
|---|---|---|---|---|---|
| 1 | Você precisa registrar uma venda. Mostre onde começaria. | Tela 1, Operadora Teste | Identifica Nova venda ou Iniciar venda | Tempo, erro, hesitação, releitura, orientação | Acesso RF04 e RNF04 |
| 2 | Registre uma venda de 0,500 kg de pão francês e confira o valor antes de confirmar. | Tela 2, R$ 20/kg, saldo 5 kg | Descreve/aponta seleção, quantidade, inclusão, total R$ 10 e confirmação | Confusão preço/quantidade/unidade, repetição, orientação | RF03, RF04 e RNF04 |
| 3 | Verifique se a venda foi concluída, informe quanto restou e mostre como iniciaria outra. Explique como reconheceu o resultado. | Tela 3, DEMO-001 | Identifica sucesso por texto/símbolo, saldo 4,500 kg e Nova venda | Confusão entre saldos, tentativa de confirmar novamente, dependência da cor | RF04, conferência RF05 e RNF04 |

Como o formulário é estático e pré-preenchido, a tarefa 2 não comprova preenchimento independente em interface interativa. Se isso for exigido pela avaliação, será necessário criar protótipo clicável ou aplicação antes de testar essa competência.

## Exatamente três dimensões de decisão

| Dimensão | Métrica/limite | Procedimento | Aprovação | Correção |
|---|---|---|---|---|
| Usabilidade | 100% = 3 de 3 sem ajuda | Uma tentativa por tarefa; releitura e autocorreção permitidas; orientação é ajuda; resultado errado/incompleto é falha | Todas sem orientação | Rever rótulos, instruções e navegação; repetir com nova versão |
| Eficiência | Tarefa 2 até 120 segundos | Iniciar após leitura e terminar na confirmação correta e apresentação do resultado; esclarecimentos não pausam; descontar só troca de imagens, registrando-a | Correta, autônoma e no limite | Reduzir etapas/ambiguidade; repetir nas mesmas condições |
| Satisfação | Nota mínima 4 em 1–5 | Pergunta neutra ao final, sem sugerir nota | 4 ou 5 | Analisar comentários e rever interface |

Pergunta completa: **Como você avalia a facilidade de entender as telas e navegar entre elas para realizar as tarefas?**

Escala: 1 Muito difícil; 2 Difícil; 3 Nem difícil nem fácil; 4 Fácil; 5 Muito fácil. Trata-se de percepção de facilidade, usada como critério de satisfação definido na atividade, não de instrumento padronizado de satisfação.

Taxa = tarefas sem ajuda / 3 × 100. Duas = 66,7%; uma = 33,3%. Conclusão com erro não aprova eficiência. Rodadas posteriores não apagam a primeira.

## Regra integrada

- Aceito: 3/3 sem ajuda, tarefa 2 ≤120 s, nota ≥4 e nenhuma falha crítica.
- Aceito com ajustes: cumpre todos os limites, mas há problemas menores sem comprometer compreensão, acesso ou conclusão.
- Não aceito: qualquer limite falha, ou há impossibilidade de concluir, perda de informação, resultado interpretado incorretamente ou alerta inacessível. Corrigir e validar antes de implementar o fluxo afetado.

Não há compensação entre critérios. Rapidez não compensa falta de compreensão. A aceitação é do desenho, não aprovação de segurança ou operação real.

## Evidências a preservar

Resultados por tarefa, ajuda e autocorreção, tempos brutos/descontos/líquidos, nota, comentários autorizados, versão e condições. Registros públicos devem ser anonimizados e autorizados. Usar a [ficha em branco](../validacao/registro-em-branco.md), sem preencher resultados hipotéticos como se fossem observações.
