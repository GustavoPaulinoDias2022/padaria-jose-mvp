# Matriz de rastreabilidade entre necessidade, requisito e evidência

Objetivo: distinguir cobertura visual e cobertura que dependerá de código, evitando considerar um botão desenhado como comprovação de uma regra implementada.

| Necessidade ou risco | Requisito | Entidades/camada | Representação nas telas | Verificação futura |
|---|---|---|---|---|
| Restringir registros à responsável | RF01, RNF01 | Usuário; autorização no servidor | Tela 1 mostra estado autenticado e Sair; login não foi desenhado | CT01/CT02 e acesso direto sem autorização; testar logout real |
| Organizar produtos usados nas vendas | RF02 | Produto; form, negócio e persistência | Tela 1 oferece Produtos; formulário de cadastro fora das três capturas | CT03/CT04; testar gravação e rejeição de dados inválidos |
| Conhecer quantidades disponíveis | RF03 | Produto; consulta e apresentação | Tela 2 mostra saldo do produto selecionado; listagem completa fora das capturas | CT05; comparar interface com base conhecida |
| Evitar anotações separadas de venda e estoque | RF04 | Venda, ItemVenda, Produto, Usuário; negócio e transação | Tela 2 confirma; tela 3 mostra resultado fictício | CT06/CT07/CT10; conferir banco e saldos |
| Evitar vendas duplicadas ou saldo negativo | RF04, RNF02 | Chave única e controle de concorrência no servidor/banco | Apenas mensagens e continuidade planejadas; imagens não comprovam proteção | CT08–CT12 com reenvio, conflito, concorrência e falha de rede |
| Conferir vendas anteriores | RF05 | Venda, ItemVenda e Usuário | Tela 3 oferece Ver histórico e resumo da venda atual; histórico completo não desenhado | CT13; verificar preço histórico após mudança do cadastro |
| Localizar vendas por data | RF06 desejável | Venda; consulta | Fora do protótipo | CT14, somente após implementar função opcional |
| Proteger entradas e informações | RNF02 | Todas as entradas; validação e persistência | Tela 2 tem rótulos e instrução, sem comprovar tratamento no servidor | Testes diretos de entradas, SQLi/XSS/CSRF e revisão de configuração |
| Usar em aparelho disponível sem instalação específica | RNF03 | Apresentação web e implantação | Três capturas desktop; celular ainda não demonstrado | Reproduzir instalação e uso no aparelho confirmado |
| Consultar estoque em tempo aceitável | RNF03 | Consulta, índices e recursos estáticos | Não mensurável em PNG | Protocolo: mediana de cinco medições ≤3 s nas condições definidas |
| Reconhecer ações e estados sem depender só da cor | RNF04 | Apresentação | Rótulos e ícones nas três telas; sucesso por texto, símbolo e cor na tela 3 | Tarefas externas, contraste medido, teste de teclado/zoom e semântica |
| Apoiar autonomia e produtividade local | ODS 8 / meta 8.2 | Solução completa e uso real | Intenção de simplificar tarefas | KPIs após implantação e comparação com linha de base; sem resultados atuais |

## Cobertura e decisões

- As capturas cobrem o caminho menu → nova venda → resultado de sucesso.
- Cadastro, login, consulta completa de estoque/histórico e cenários de erro são requisitos ou destinos planejados, não telas já construídas.
- Estados Processando, sessão expirada, estoque insuficiente e resultado desconhecido após falha de rede precisam de desenho/interação antes da validação específica desses estados.
- Os testes funcionais CT01–CT14 estão definidos em [cenários de aceitação](11-cenarios-de-aceitacao.md), não implementados como testes automatizados.
- O aparelho e a conectividade reais precisam ser confirmados; a captura desktop não comprova adequação móvel.
- O filtro RF06 pode ser adiado sem impedir o fluxo principal. Edição, reposição e correção continuam pendências de detalhamento, não funcionalidades implicitamente concluídas.

## Manutenção da matriz

Cada nova funcionalidade deve ligar necessidade, requisito, entidade, interface e critério de teste. Ao implementar, registrar o commit e a evidência real no caso correspondente. Mudanças de escopo exigem atualizar requisitos e plano de teste, sem reclassificar automaticamente propostas como entregas.
