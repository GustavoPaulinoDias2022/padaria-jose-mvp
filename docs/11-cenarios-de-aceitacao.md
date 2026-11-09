# Cenários de aceitação do fluxo funcional

**Plano de testes; nenhum cenário abaixo foi executado.** Estes exemplos tornam verificáveis os requisitos existentes, sem representar funcionalidades já implementadas ou novos resultados de campo.

## Preparação

Usar ambiente isolado, conta fictícia ativa com permissão de proprietária, outra conta sem essa permissão e produtos fictícios. Restaurar os saldos antes de cada cenário. A conferência da interface deverá ser acompanhada de consulta ao banco de teste; uma mensagem de sucesso sozinha não comprova persistência.

| Caso | Requisito | Contexto e ação | Resultado esperado e evidência |
|---|---|---|---|
| CT01 | RF01 | Dada uma conta ativa autorizada, quando informa credenciais válidas | Acesso ao menu e às funções protegidas; registrar resposta e estado da sessão, sem expor credenciais. |
| CT02 | RF01 | Dadas credenciais inválidas, quando tenta entrar | Sem sessão autenticada, mensagem genérica e nenhum acesso aos dados. |
| CT03 | RF02 | Dada conta autorizada, quando cadastra Pão teste, R$ 20,00/kg e saldo 5,000 kg | Um produto gravado com os valores informados; consultar novamente para conferir. |
| CT04 | RF02 | Quando envia diretamente ao servidor preço zero, estoque negativo ou 1,500 de produto UN | Rejeição de cada entrada inválida, com orientação, sem criar produto. Executar cada variação separadamente. |
| CT05 | RF03 | Dado um produto conhecido, quando consulta o estoque | Nome, preço, unidade, saldo e situação iguais ao banco. |
| CT06 | RF04 | Dado saldo 5,000 kg e preço R$ 20,00/kg, quando vende 0,500 kg | Uma venda e um item, total R$ 10,00, saldo 4,500 kg e responsável correto. |
| CT07 | RF04 | Dado saldo 3 UN, quando tenta vender 5 UN | Estoque insuficiente informado; nenhuma venda/item criado e saldo permanece 3. |
| CT08 | RF04 | Dada operação já concluída, quando reenvia o mesmo conteúdo com a mesma chave | Retorna a referência ao resultado existente, sem nova venda ou segunda baixa. |
| CT09 | RF04 | Quando envia conteúdo diferente usando uma chave já utilizada | Recusa conflito sem alterar a venda original ou o estoque. |
| CT10 | RF04 | Dada venda com dois itens, quando ocorre falha controlada depois de uma gravação e antes do fim da transação | Rollback integral: sem venda/item parcial, saldos originais preservados. Usar injeção de falha somente no ambiente de teste. |
| CT11 | RF04 | Dado saldo 3 UN, quando duas solicitações independentes tentam vender 2 UN ao mesmo tempo | Somente uma confirma; outra é recusada; saldo final 1 e apenas uma venda. Executar com conexões/transações independentes. |
| CT12 | RF04 | Dada confirmação persistida cuja resposta se perdeu, quando consulta ou repete a operação com a mesma chave | Identifica a mesma venda e não a duplica. Mensagem de rede não deve afirmar fracasso definitivo. |
| CT13 | RF05 | Dada venda a R$ 20,00/kg, quando o preço atual do produto muda e a venda antiga é consultada | Histórico mantém preço praticado, quantidade, unidade e total originais. Preparar a mudança na base de teste enquanto edição não tiver requisito próprio. |
| CT14 | RF06 | Dado filtro desejável implementado, quando seleciona intervalo válido ou invertido | Datas extremas incluídas no intervalo válido; intervalo invertido recusado. Adiado enquanto RF06 não for implementado. |

## Conferências complementares do RF04

- Preço enviado pelo navegador não substitui o preço consultado e validado pelo servidor.
- Produto inativo, inexistente, quantidade zero ou negativa e fração em UN devem ser recusados.
- O identificador do responsável deve vir da sessão autorizada, não de um campo livre controlado pelo navegador.
- O total deve usar aritmética decimal; a regra de arredondamento deve ser definida antes dos testes com valores fracionários que gerem mais de duas casas.
- A transação deve combinar autorização, integridade e controle de concorrência; a existência de um bloco atômico não comprova essas três propriedades.

## Registro e aprovação futura

Para cada execução, preservar caso, versão/commit, ambiente, dados iniciais, ação, resultado esperado, resultado observado, status e evidência sem segredos. Qualquer divergência em CT06–CT13 exige correção antes do uso real. Falhas de autorização ou validação bloqueiam a liberação mesmo quando a tela parece correta.

O protótipo de imagens pode apoiar somente compreensão visual dos cenários. Os testes de banco, concorrência, rede, autenticação e rollback exigem aplicação implementada.
