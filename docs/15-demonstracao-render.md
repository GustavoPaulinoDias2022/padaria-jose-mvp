# Demonstração gratuita no Render

## Estado e limites

Configuração preparada; ainda não há serviço provisionado nem URL pública verificada. O arquivo render.yaml descreve uma aplicação Django e um PostgreSQL gratuitos na mesma região, usando a branch de implementação. A criação depende de acesso à conta Render e confirmação da disponibilidade gratuita no painel. Não autoriza plano pago.

Conforme a [documentação oficial do plano gratuito](https://render.com/docs/free), a aplicação pode suspender após 15 minutos sem tráfego e o PostgreSQL gratuito expira após 30 dias. Portanto, esta modalidade atende à demonstração acadêmica temporária com dados fictícios. Não atende à operação contínua da padaria. Registrar a data real de expiração após a criação e preservar exportação antes desse prazo.

## Implantação reproduzível

1. Criar um Blueprint a partir de render.yaml no repositório público, selecionando feat/mvp-django-testes. Conferir que ambos os serviços permanecem gratuitos antes de confirmar.
2. Preencher DJANGO_SECRET_KEY com segredo aleatório estável de pelo menos 50 caracteres. Informar INITIAL_OWNER_USERNAME e INITIAL_OWNER_PASSWORD como segredos no painel, usando conta fictícia e senha forte de pelo menos 15 caracteres; nunca versionar esses valores.
3. O Blueprint conecta DATABASE_URL ao PostgreSQL. O runtime é Python 3.13.13. build.sh instala requisitos fixados, coleta estáticos e executa check --deploy. start.sh aplica migrações e inicia Gunicorn em uma instância com duas threads.
4. bootstrap_owner cria uma conta comum com a permissão de operação. Reexecução preserva a senha existente; não há senha padrão. Remover as duas variáveis INITIAL_OWNER após o provisionamento. SEED_DEMO_DATA=1 cria quatro produtos fictícios sem sobrescrever os saldos existentes; desativar após a carga.
5. RENDER_EXTERNAL_HOSTNAME adiciona somente o domínio exato à lista permitida. TRUST_HTTPS_PROXY=1 depende do proxy da hospedagem sobrescrever X-Forwarded-Proto; não habilitar em servidor exposto diretamente. Não confiar em X-Forwarded-For fornecido pelo cliente para contornar bloqueios.

## Verificações realizadas na preparação

Em 09/11/2026, a execução local SQLite encontrou 58 testes: 57 aprovados e um teste de concorrência reservado ao PostgreSQL ignorado, em 12,360 segundos. A cobertura local de linhas e ramificações do escopo Python instrumentado foi 100%. Esses números não substituem uma nova execução PostgreSQL do commit de implantação.

Testes adicionados verificam healthcheck GET com consulta ao banco, erro 503 sem detalhes internos, recusa de POST, criação inicial sem senha padrão, rejeição de senha fraca/configuração incompleta, permissões mínimas, preservação da senha e carga fictícia opcional sem sobrescrever saldo. A configuração de produção rejeita PostgreSQL sem TLS. Nenhuma credencial de hospedagem foi gravada no código.

## Aceitação após publicação

Preservar o commit implantado, URL e resultado real do deploy. Verificar HTTPS, /healthz/ com status 200, CSS local, login válido/inválido, bloqueio sem autenticação, CSRF, encerramento da sessão e venda fictícia com baixa correta e proteção contra repetição. Confirmar comportamento do bloqueio de login atrás do proxy: o endereço remoto pode representar o proxy e produzir bloqueio compartilhado. Isso exige teste no provedor antes de liberar acesso mais amplo. Não interpretar healthcheck ou check --deploy como auditoria completa.

Backups/restauração, desempenho móvel real, acessibilidade assistiva e validação com a parceira continuam pendentes. A preparação local não comprova funcionamento em produção.

Referências: [Django no Render](https://render.com/docs/deploy-django), [Blueprint](https://render.com/docs/blueprint-spec) e [healthchecks](https://render.com/docs/health-checks).
