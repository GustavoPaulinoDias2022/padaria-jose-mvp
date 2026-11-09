# Executar e testar o MVP

Requer Python 3.13. Não há usuário/senha padrão, dados pessoais ou conta de demonstração automaticamente criada. Os valores presentes nos testes são fictícios e não são credenciais para operar a aplicação.

## Instalação local — Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:DJANGO_SECRET_KEY = (.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))")
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py setup_owner minha_conta
.venv\Scripts\python.exe manage.py collectstatic --noinput
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Escolha a senha quando solicitada, com no mínimo 15 caracteres. O comando valida a senha e concede apenas a permissão de operação, sem tornar a conta superusuária. Não passe a senha em argumento de linha de comando ou mensagem.

A chave aleatória do exemplo dura nessa sessão de terminal. Para manter sessões entre reinícios, configure uma chave estável em armazenamento local seguro, sem versioná-la. O arquivo .env.example é apenas documentação; o programa lê variáveis de ambiente e não carrega .env automaticamente.

## Linux

Usar `python3.13 -m venv .venv` e `.venv/bin/python` nos comandos equivalentes. Definir as variáveis via ambiente do shell ou painel da hospedagem. Instalar requirements.txt para runtime e requirements-dev.txt para testes.

## Primeiro uso

Abrir http://127.0.0.1:8000, entrar com a conta criada e cadastrar produtos fictícios ou os dados autorizados pela parceira. Em Nova venda, escolher primeiro a quantidade de produtos diferentes; preencher itens; usar Conferir total; revisar e Confirmar venda. Ao cancelar, nada é gravado. A confirmação revalida preços e saldos no servidor.

A edição de produto permite ajustes manuais de saldo, com aviso explícito. Ainda não há histórico específico desses ajustes. Produtos vendidos preservam nome/preço/unidade nos itens históricos e não podem mudar de unidade. Não há exclusão de vendas confirmadas ou emissão fiscal.

## Testes e cobertura

```powershell
.venv\Scripts\python.exe manage.py collectstatic --noinput
.venv\Scripts\python.exe -m coverage run manage.py test --settings=config.testing --verbosity=2
.venv\Scripts\python.exe -m coverage report
.venv\Scripts\python.exe -m coverage json -o coverage.json
.venv\Scripts\python.exe -m coverage html
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

O banco de teste é criado e destruído automaticamente. Não utilizar DATABASE_URL apontando para produção para rodar testes. HTML detalhado fica em htmlcov/index.html e não precisa ser versionado. A configuração de cobertura está em .coveragerc.

## PostgreSQL de desenvolvimento ou CI

Configurar DATABASE_URL para um banco isolado e conta com permissão de criar o banco de teste. Por exemplo, usar o painel seguro de ambiente para informar a URL, sem copiá-la para o repositório. O workflow [tests.yml](../.github/workflows/tests.yml) cria um PostgreSQL descartável, usa credenciais exclusivamente fictícias de CI e executa também o teste concorrente.

## Implantação futura

1. Definir APP_ENV=production, DJANGO_SECRET_KEY aleatória estável, DJANGO_ALLOWED_HOSTS e DATABASE_URL PostgreSQL com TLS.
2. Configurar CSRF_TRUSTED_ORIGINS se exigido pela origem HTTPS real. TRUST_HTTPS_PROXY=1 somente se o proxy confiável sobrescrever o cabeçalho indicado na configuração.
3. Instalar requirements.txt, aplicar migrações, coletar estáticos e iniciar `gunicorn config.wsgi:application` em Linux. Não usar runserver em produção.
4. Criar conta via setup_owner em ambiente protegido; verificar `python manage.py check --deploy`.
5. Revisar política de tentativas por IP atrás do proxy, retenção dos registros do django-axes, backup/restauração e testes de rede, acesso e acessibilidade.

Não existe implantação de produção nesta entrega. O bloqueio de login pode ser administrado com `python manage.py axes_reset` por quem possui acesso autorizado ao servidor; isso limpa bloqueios e não deve ser exposto na interface ou executado indiscriminadamente.
