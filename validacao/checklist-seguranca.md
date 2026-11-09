# Checklist de liberação — RNF01 e RNF02

**Estado de todos os itens: não executado.** Este documento transforma controles planejados em verificações para a futura aplicação. Não é certificado de segurança nem resultado de auditoria do sistema.

Executar somente em ambiente próprio/autorizado, com dados fictícios e sem atingir sistemas de terceiros. Não anexar credenciais, cookies, tokens, dumps ou dados pessoais às evidências públicas.

## Identificação da rodada

- Versão/commit da aplicação: pendente
- Ambiente isolado e autorização: pendente
- Responsável/data: pendente
- Versões de Python, Django, driver e banco: pendente
- Resultado geral e pendências: pendente

| ID | Verificação | Evidência esperada | Estado |
|---|---|---|---|
| SEG01 | Login válido, inválido e conta inativa | Somente conta ativa autorizada acessa; resposta inválida não revela existência da conta | Não executado |
| SEG02 | Acesso direto a cada operação sem login e com conta sem permissão | Cadastro, consulta, venda e histórico recusados; banco sem alteração | Não executado |
| SEG03 | Armazenamento de senha | Campo com identificação pbkdf2_sha256; senha não legível; não publicar hash real | Não executado |
| SEG04 | Validação da senha na definição inicial | Mínimo de 15 caracteres e rejeição conforme validadores configurados, aplicada também no caminho de criação adotado | Não executado |
| SEG05 | Cinco falhas em 15 minutos e nova tentativa | Bloqueio temporário de 15 minutos e liberação após prazo; registrar também teste do limite por IP quando definido | Não executado |
| SEG06 | Sessão, cookies e logout | Secure/HttpOnly/SameSite configurados; rotação no login; cookie anterior não reutilizável após logout | Não executado |
| SEG07 | Inatividade de 30 minutos | Operação exige novo login após inatividade; requisições ativas não são confundidas com tempo absoluto de sessão | Não executado |
| SEG08 | CSRF e métodos HTTP | Requisição de alteração sem token válido recusada; GET não cria venda nem altera estoque | Não executado |
| SEG09 | Entradas enviadas diretamente ao servidor | Valores negativos, não numéricos, produto inativo e fração em UN recusados sem gravação parcial | Não executado |
| SEG10 | ORM e SQL injection | Revisão sem concatenação de entrada em SQL; payloads não executam comandos nem expõem SQL | Não executado |
| SEG11 | XSS e CSP | HTML não permitido rejeitado ou exibido como texto; nenhum script executado; política de conteúdo inspecionada | Não executado |
| SEG12 | Reenvio, concorrência e rollback | Uma operação não duplica; saldo nunca negativo; falha no meio da gravação desfaz alterações | Não executado |
| SEG13 | Segredos e arquivos públicos | Nenhum segredo versionado; arquivos de ambiente/backups inacessíveis pela web; credenciais fora de URLs/logs | Não executado |
| SEG14 | Configuração de implantação | DEBUG=False, hosts explícitos, HTTPS e check --deploy com alertas tratados | Não executado |
| SEG15 | Erros e logs | 404/500 sem rastreamento interno, senha, token ou consulta; logs restritos e sem dados desnecessários | Não executado |
| SEG16 | Dependências | Versões completas fixadas, fontes oficiais, relatório de auditoria e avisos do Bootstrap revisados | Não executado |
| SEG17 | Banco, backup e restauração | Conta de menor privilégio; backup restrito; restauração em ambiente isolado demonstrada | Não executado |
| SEG18 | Minimização e autorização de evidências | Sem CPF/telefone de clientes; consentimento e identificação da participante fora do Git público | Não executado |

## Decisão de liberação

Falhas de autenticação/autorização, injeção, exposição de segredos, duplicidade ou inconsistência de estoque bloqueiam a liberação até correção e repetição dos testes afetados. Outros achados devem ser avaliados quanto ao impacto, registrados e tratados antes da liberação quando relevantes. Uma ferramenta sem alertas não substitui revisão do comportamento e configuração.

Itens realmente não aplicáveis devem indicar o motivo e a versão avaliada, em vez de receber aprovação automática. Uploads e chamadas para URLs externas não são funcionalidades previstas; se adicionados, o plano deverá incluir controles específicos.

## Modelo de registro de achado

- ID / controle relacionado: pendente
- Comportamento observado e impacto: pendente
- Passos de reprodução com dados fictícios: pendente
- Correção e commit: pendente
- Reteste / evidência sanitizada: pendente
- Decisão e responsável: pendente

Referências de escopo: [requisitos](../docs/05-requisitos.md), [ameaças OWASP](../docs/06-seguranca.md) e [cenários funcionais](../docs/11-cenarios-de-aceitacao.md).
