# Ameaças e revisão de segurança

Referência: [OWASP Top 10:2025](https://top10.owasp.org/2025/). Testes futuros serão executados somente no ambiente próprio ou autorizado do MVP, não contra MarketUP, Bling ou outros terceiros.

| Ameaça | Categoria | Ativo/fluxo | Controle planejado | Verificação prevista |
|---|---|---|---|---|
| SQL injection | A05 Injection | Produtos, consultas, vendas | ORM/parametrização, validação no servidor | Entradas SQL não executam comandos nem expõem erro interno. |
| XSS armazenado/refletido | A05 Injection | Nome de produto e mensagens | Autoescape, texto sem HTML, sem safe em entradas, CSP | Scripts/eventos rejeitados ou mostrados como texto; inspecionar CSP. |
| Acesso indevido/CSRF | A01 Broken Access Control | Todas as operações protegidas | Negar por padrão; autenticar e autorizar; POST/CSRF | Anônimo e conta sem permissão não alteram dados; CSRF inválido recusado. |
| Força bruta e sessão reutilizada | A07 Authentication Failures | Login/sessão | RNF01, limitador adicional, hash e expiração | Testar limites, sessão antiga, logout, cookies e hash. |
| Segredos e erros expostos | A02 Security Misconfiguration | Credenciais, SECRET_KEY, arquivos/erros | Ambiente, DEBUG=False, menor privilégio, erros genéricos | Revisar repositório e configuração; 404/500; check --deploy. |
| Dependências vulneráveis | A03 Software Supply Chain Failures | Python/Django/Psycopg/Bootstrap | Versões fixadas, fontes oficiais, auditoria e atualização | Relatório de dependências e avisos de segurança; regressão após atualização. |

## Revisão proporcional desta entrega

**Escopo real:** Markdown, imagens de protótipos e pacote para GitHub. Não existe código cliente/servidor executável, banco configurado, credencial de hospedagem ou site publicado nesta entrega. Os mecanismos descritos são especificações, não controles já eficazes.

### Cuidados aplicados ao material público

- Nome completo da participante e seus contatos omitidos dos documentos de publicação.
- Imagens com conta e transação fictícias; geração de imagem declarada.
- Materiais curriculares integrais e arquivos pessoais não incluídos.
- Arquivos de ambiente, dumps, backups, mídia privada e consentimentos ignorados pelo Git.
- Evidências inexistentes não inventadas; resultados de testes deixados em branco.
- Não se atribui licença de terceiros nem se publica licença aberta sem escolha do autor.

O .gitignore não é controle de acesso e não retira segredos já versionados. Antes de cada publicação, revisar o conteúdo efetivamente incluído.

### Ainda não testado / ação antes de produção

1. Implementar e testar RNF01–RNF04, inclusive acesso direto a endpoints e inatividade no servidor.
2. Testar concorrência e atomicidade da baixa de estoque, reenvio e resultado desconhecido após falha de rede.
3. Definir arredondamento monetário, reposição de estoque e correção operacional de vendas.
4. Verificar HTTPS, cookies, CSRF, CSP, hosts, segredos, permissões do banco e respostas de erro.
5. Auditar dependências reais e configurações da hospedagem; corrigir achados relevantes.
6. Proteger backups, definir retenção e executar restauração.
7. Verificar acessibilidade e desempenho no dispositivo e rede documentados.

Uploads, SSRF por busca remota, pagamentos e integrações externas não são previstos no núcleo atual. Se forem acrescentados, exigirão novos controles. CORS de uma API entre origens não é necessário na aplicação de mesma origem proposta; não abrir origens indiscriminadamente. Não há publicação em produção autorizada por este planejamento documental.

## Registro de auditoria

O arquivo [VERIFICACAO-LOCAL.md](../VERIFICACAO-LOCAL.md) registra somente verificações realizadas no pacote documental. Não equivale a pentest, auditoria do aplicativo ou garantia de segurança.
