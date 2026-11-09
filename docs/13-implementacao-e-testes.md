# Implementação e evidências de teste

Data da execução local: 08/11/2026 (America/Sao_Paulo). Esta atualização sucede o planejamento documental e não representa validação externa ou implantação em produção.

## Entregue em código

- Aplicação Django em camadas: forms, serviços transacionais, models/ORM e templates.
- Conta local sem senha padrão, criada com validação de senha e permissão específica.
- Login/logout, autorização no servidor e inatividade de 30 minutos.
- Produtos, edição/desativação, consulta paginada e busca.
- Venda de até 20 produtos diferentes, prévia sem gravação e confirmação com baixa de estoque.
- Preços e totais calculados no servidor, arredondamento ROUND_HALF_UP por item e total como soma dos subtotais.
- Chave UUID e fingerprint do conteúdo para reenvio idempotente; proteção contra reuso com outro conteúdo/operador.
- Banco com restrições e transação integral; bloqueios PostgreSQL e atualização condicional de saldo.
- Histórico com nome, unidade e preço do item preservados.
- Layout responsivo com CSS local, sem JavaScript ou recursos externos. Paginação de 25 registros.

## Resultado local

- Python 3.13.13, Django 5.2.19, coverage.py 7.17.2, Windows, SQLite de teste em memória.
- 51 testes descobertos: 50 executados com sucesso e 1 ignorado por exigir PostgreSQL real.
- Última execução local registrada: aproximadamente 8,5 segundos (tempo da suíte, não carregamento de página).
- Cobertura de código de linhas e ramificações: **100% no escopo instrumentado**.
- `manage.py check`, `makemigrations --check --dry-run` e `check --deploy` sem apontamentos na configuração avaliada.
- Auditoria pip-audit das dependências runtime aplicáveis ao Windows: sem vulnerabilidades conhecidas informadas pela base consultada. Gunicorn não é instalado no Windows e sua auditoria será feita no CI Linux.

O resultado será atualizado se a execução final ou o CI apresentar diferença. O teste de concorrência não é considerado aprovado por estar ignorado no SQLite.

## Escopo da cobertura

Inclui módulos próprios `loja` e `config`, com medição de ramificações habilitada. Exclui migrações geradas, código dos testes e pontos de entrada WSGI/ASGI. Não mede templates, CSS, bibliotecas Django/axes, comportamento de navegador ou infraestrutura. 100% de cobertura não significa ausência de defeitos, segurança absoluta ou conclusão de todos os requisitos não funcionais.

Os testes verificam regras de venda e prévia, autorização direta, autenticação, hash, CSRF, limite de tentativas e liberação, sessão expirada/logout, reenvio/conflito, rollback, estoque insuficiente, histórico, escape de saída, busca com conteúdo SQL e configurações de produção. Configurações são carregadas com dados fictícios para verificar falha segura na ausência de chave/banco.

## Evidências reproduzíveis

- [Resumo de cobertura](../relatorios/coverage.txt)
- [Cobertura JSON](../relatorios/coverage.json)
- [Auditoria de dependências](../relatorios/dependencias.json)
- [Comandos de execução](14-execucao.md)
- [Workflow PostgreSQL](../.github/workflows/tests.yml)

## Segurança: controles verificados e limites

Testes efetivos cobrem validação no servidor, autorização de operações, hash PBKDF2, proteção CSRF, escape de texto, bloqueio após falhas, expiração/logout, reenvio e rollback. A auditoria não encontrou vulnerabilidades conhecidas no conjunto Windows consultado. Configuração de cookies seguros e CSP foi inspecionada nas respostas de teste; HTTPS real e proxy da hospedagem ainda não foram verificados.

Antes de produção: validar TLS real e rede/banco, isolamento de infraestrutura, retenção/limpeza de logs de tentativas, restauração de backups, concorrência em PostgreSQL, usuário de banco com menor privilégio e configuração do IP confiável atrás do proxy. A limitação por IP não deve confiar cegamente em cabeçalhos enviados pelo cliente.

Não há coleta de dados de clientes, upload, fetch de URLs externas, pagamentos ou API entre origens. Acesso a arquivos locais e publicação de dados pessoais não foram acrescentados. Credenciais de testes são fictícias e não habilitam uma conta de produção.

## Limitações funcionais e validação pendente

O formulário usa renderização no servidor e prévia explícita, sem os efeitos dinâmicos das imagens. Alterar quantidade de linhas antes do preenchimento abre um formulário vazio. O ajuste de estoque não tem trilha própria; cancelamento/estorno de venda e filtro por período não foram implementados. Reenvio após queda da rede exige manter o mesmo formulário/chave.

Teclado, zoom, contraste medido, leitor de tela, experiência no aparelho da proprietária, meta de três segundos na rede proposta e indicadores sociais precisam de validação específica. Os testes HTML confirmam elementos e rótulos, mas não substituem esses ensaios.
