# Requisitos e critérios verificáveis

Todos os requisitos estão planejados; não há evidência de implementação.

## Funcionais

| ID | Prioridade | Comportamento e regra | Evidência de cumprimento | Dependência |
|---|---|---|---|---|
| RF01 | Obrigatório | Autenticar proprietária com conta ativa, credenciais válidas e permissão. | Login válido acessa; inválido e acesso anônimo não acessam operações protegidas. | Nenhuma |
| RF02 | Obrigatório | Cadastrar produto: nome, preço positivo, UN/KG, estoque não negativo; UN somente inteiro. | Cadastro válido gera um registro; inválido explica erro sem gravar. | RF01 |
| RF03 | Obrigatório | Consultar nome, preço, unidade, quantidade e situação dos produtos. | Dados exibidos correspondem à base conhecida de teste. | RF01, RF02 |
| RF04 | Obrigatório | Registrar venda de produtos ativos com quantidade positiva disponível, total no servidor e baixa atômica/idempotente. | Saldo 3, venda 2 deixa 1; venda 4 é recusada sem alterações; reenvio não duplica. | RF01, RF02 |
| RF05 | Obrigatório | Consultar histórico/detalhes: data, responsável, itens, quantidades, preços e total. | Venda aparece e preço histórico não muda ao editar produto. | RF01, RF04 |
| RF06 | Desejável | Filtrar histórico por datas inicial e final inclusivas. | Retorna somente período; início posterior ao fim é recusado. | RF05 |

RF01–RF05 permitem registrar e recuperar informações com acesso controlado. RF06 facilita navegação mas não é necessário para validar integração entre venda e estoque. Ordem: autenticação, produtos, estoque, venda integrada e histórico; filtro depois.

Edição/desativação de produtos foi prevista nas histórias, mas precisa ganhar requisitos próprios antes de ser codificada. Não está implementada e não deve ser agrupada ao teste de cadastro. Necessidades de reposição e correção também exigem detalhamento.

## Histórias de usuário

1. Como proprietária, quero cadastrar e editar produtos, preços e quantidades para manter informações organizadas e atualizadas.
2. Como proprietária, quero registrar vendas com baixa automática para reduzir erros e alterações manuais duplicadas.
3. Como proprietária, quero consultar estoque e histórico para identificar reposição e acompanhar o movimento.

## Fora do escopo

- Emissão fiscal e integração contábil.
- Loja virtual, pagamentos digitais e delivery.
- Operação offline completa e sincronização entre dispositivos.

## RNF01 — Acesso e autenticação

Todas as operações de produtos, vendas, estoque e histórico exigirão conta ativa e autorização de proprietária, verificadas no servidor. Não haverá cadastro público. Senha definida pela participante em configuração inicial, mínimo de 15 caracteres, com validação contra senhas comuns e similares ao username; transmitida apenas em HTTPS e ausente de URLs/logs.

Armazenar com PBKDF2-HMAC-SHA256, salt e fator de trabalho da versão atualizada do Django 5.2, via PBKDF2PasswordHasher e funções nativas. **Nunca texto limpo, MD5 ou SHA-1.** Hash é de sentido único; criptografia reversível permite recuperar conteúdo com chave e não é a estratégia de armazenamento de senhas.

Sessões no servidor; cookies Secure, HttpOnly e SameSite=Lax; rotação no login, CSRF e logout com invalidação. Inatividade de 30 minutos será verificada no servidor, não presumida de uma configuração de expiração absoluta.

Limitação adicional: cinco falhas por conta em 15 minutos geram bloqueio por 15 minutos, com limite complementar por IP a definir/testar. Backend padrão do Django não limita tentativas. Considerar confiança no proxy e risco de bloqueio indevido da única usuária.

Aceitação: inspecionar hash no banco, testar login válido/inválido, autorização direta, CSRF, HTTPS/cookies, bloqueio e liberação, expiração e impossibilidade de reutilizar sessão após logout.

## RNF02 — Proteção de dados e OWASP

Validação no cliente é auxílio; servidor revalida tipos, limites, produtos ativos, preços e disponibilidade. ORM/SQL parametrizado sem concatenação. Templates com autoescape; campos de texto simples rejeitam HTML; não usar safe em entradas. CSP restritiva, preferindo estáticos locais e sem scripts inline.

Autorizar cada operação e exigir POST/CSRF para alterações. Banco acessível pela aplicação com menor privilégio. Minimizar dados pessoais, proteger backups, segredos por ambiente fora do repositório. HTTPS, DEBUG=False, hosts explícitos, erros genéricos e logs sem senhas/tokens. Dependências fixadas e auditadas.

Aceitação: rejeição de entradas inválidas enviadas diretamente, testes de SQLi/XSS sem execução, bloqueio de acesso e CSRF, ausência de arquivos sensíveis públicos, ausência de segredos no repositório, check --deploy e auditoria com pendências avaliadas antes da liberação.

## RNF03 — Portabilidade e desempenho

Meta, condições, hospedagem e procedimento detalhados em [arquitetura](03-arquitetura-e-tecnologias.md). Página de estoque, 25 produtos por página, base 500 produtos/5.000 vendas; Android 2 GB/quatro núcleos; rede 1,5 Mbps/750 kbps/150 ms. Uma execução de aquecimento e cinco medições com cache do navegador desativado; mediana até 3 s. Cold start registrado separadamente. Instalação documentada e reproduzida nos ambientes previstos.

## RNF04 — Acessibilidade

Aplicar ao menu, cadastro, venda, estoque e resultados:

- Botões/ações com alvo mínimo de 44 × 44 pixels CSS.
- Texto com contraste mínimo de 4,5:1; informação visual necessária de controles com 3:1.
- Ampliação a 200% sem perda de conteúdo/funcionalidade.
- Teclado com ordem lógica e foco visível, sem armadilhas.
- Rótulos associados aos campos; erros com problema e correção.
- Alertas com texto e símbolo, além da cor; anúncios dinâmicos acessíveis na implementação.

A referência de 44 px é uma escolha do projeto, não alegação de que seja o mínimo AA universal da WCAG. Verificar contraste/dimensões, teclado, zoom, semântica e tecnologias assistivas na interface real. Imagens não comprovam conformidade.

## Coerência final

Necessidade: atualização integrada de registros manuais. Decisão: transação de venda e estoque na camada de negócio/persistência. Tecnologia: templates/Bootstrap para navegação focada. Entidade essencial: ItemVenda preserva quantidade, unidade e preço. Limite: emissão fiscal excluída. Cenário de aceitação: saldo 3 e tentativa de vender 5 devem recusar toda a operação sem gravar nem reduzir estoque.
