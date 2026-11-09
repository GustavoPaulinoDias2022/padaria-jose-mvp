# Ajuste de orientação da quantidade e da prévia

Origem: hipótese de usabilidade levantada na conversa de planejamento. Não houve confirmação de entrevista, rodada de validação ou relato real da proprietária que motivasse esta alteração.

## Alteração implementada

- O help_text do DecimalField em SaleRowForm passa a exemplificar 0,500 kg como meio quilo e distinguir a quantidade inteira para UN.
- O template informa que Conferir total não persiste a venda e não atualiza estoque.
- A prévia identifica explicitamente a venda como ainda não registrada; Confirmar venda informa o efeito de persistência e baixa.
- aria-describedby associa os botões às instruções, e a prévia recebe identificação semântica de status. O anúncio efetivo em leitor de tela requer teste específico.

As regras de preview_sale e register_sale permanecem separadas. A alteração é de comunicação na camada de apresentação, preservando validações de Decimal no servidor e a transação na confirmação.

## Verificação

O teste de integração da prévia verifica mensagens, associações de descrição, ausência de Venda e manutenção do saldo 5,000 kg antes da confirmação. O teste de HTML verifica o exemplo e a associação da ajuda ao campo. A suíte deve ser executada na versão desta alteração; resultados anteriores de cobertura permanecem vinculados aos commits documentados.
