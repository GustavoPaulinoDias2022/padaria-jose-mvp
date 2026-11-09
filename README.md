# Padaria José — MVP de vendas e estoque

Planejamento acadêmico e protótipos visuais de uma aplicação para integrar o registro de vendas ao controle de estoque de um pequeno comércio.

**Situação atual: planejamento documentado e três imagens de protótipo. Não há aplicação Django implementada, implantação, testes executados ou validação com a participante comprovados neste repositório.**

O nome desta pasta é uma identificação técnica para o repositório. O título formal adotado na Experiência Prática 1 ainda precisa ser confirmado antes da entrega acadêmica.

## Contexto

O parceiro informado pelo estudante é a **Padaria José**, no bairro Jardim Paraíso, em Elói Mendes. O problema relatado é o uso de anotações manuais para vendas e estoque, dificultando a atualização das quantidades, a identificação de produtos em falta e o acompanhamento do movimento.

A usuária direta será a proprietária. Clientes e moradores da região são beneficiários indiretos. Seu nome completo e contatos foram omitidos desta versão pública. O curso informado é **Ciência da Computação — UNIFRAN / Cruzeiro do Sul**.

## Proposta

Aplicação web responsiva com cadastro de produtos, consulta de estoque, registro de vendas com baixa automática e histórico. O diferencial proposto é uma interface focada nessas tarefas, a ser validada com a usuária. Não foi comprovada superioridade de usabilidade em relação a sistemas existentes.

## Navegue pela documentação

| Documento | Conteúdo |
|---|---|
| [Contexto e investigação](docs/01-contexto-e-investigacao.md) | Parceiro, problema, público, diagnóstico, ODS e referências de aprendizagem |
| [Pesquisa de soluções](docs/02-solucoes-semelhantes.md) | MarketUP e Bling; evidências e posicionamento |
| [Arquitetura e tecnologias](docs/03-arquitetura-e-tecnologias.md) | Camadas, fluxo, stack, hospedagem e dependências |
| [Modelo de dados](docs/04-modelo-de-dados.md) | Entidades, atributos, relacionamentos e minimização |
| [Requisitos](docs/05-requisitos.md) | RF01–RF06, RNF01–RNF04 e critérios de aceitação |
| [Segurança e revisão](docs/06-seguranca.md) | Ameaças OWASP e auditoria proporcional ao estágio atual |
| [Protótipos](docs/07-prototipos.md) | Três telas, descrições, navegação e limitações |
| [Validação](docs/08-validacao.md) | Participação, três tarefas, métricas e regras de decisão |
| [Plano de trabalho](docs/09-plano-e-aprendizagem.md) | Cronograma, KPIs, aprendizagem e pendências |
| [Publicação e fontes](docs/10-publicacao-e-fontes.md) | Como publicar e limites das evidências |
| [Cenários de aceitação](docs/11-cenarios-de-aceitacao.md) | Casos verificáveis de cadastro, vendas, estoque e histórico, ainda não executados |
| [Matriz de rastreabilidade](docs/12-matriz-de-rastreabilidade.md) | Relação entre problema, requisitos, entidades, telas e verificações |
| [Checklist de segurança](validacao/checklist-seguranca.md) | Verificações de acesso, entradas, sessão, segredos e implantação, ainda não executadas |

## Protótipos

### Tela 1 — Menu inicial

![Menu inicial com acesso à nova venda, produtos, estoque e histórico](prototipos/tela-1-menu-inicial.png)

### Tela 2 — Nova venda

![Formulário fictício de venda de meio quilo de pão francês por dez reais](prototipos/tela-2-nova-venda.png)

### Tela 3 — Resultado da venda

![Confirmação fictícia da venda e saldo de quatro quilos e meio em estoque](prototipos/tela-3-resultado-venda.png)

As imagens foram criadas com geração de imagens assistida por IA. São propostas visuais estáticas, não capturas de um sistema em execução nem evidências de investigação em campo. Todos os dados de transações e da conta exibida são fictícios.

## Tecnologias planejadas

Python 3.13.x, Django 5.2 LTS, templates HTML, Bootstrap 5.3.x, PostgreSQL gerenciado, Psycopg 3 e Gunicorn na hospedagem Linux. Versões completas e infraestrutura serão confirmadas na implementação. Não existe instalação executável nesta entrega documental.

## Próximos passos

1. Confirmar o título acadêmico, dispositivo, conexão e requisitos com a parceira.
2. Obter consentimento e realizar a validação, preservando registros privados.
3. Ajustar as interfaces e implementar o núcleo em incrementos testáveis.
4. Verificar segurança, acessibilidade, desempenho e restauração dos backups antes de implantar.

## Privacidade e uso

Não publicar credenciais, dados pessoais de clientes, nome completo da participante, consentimentos, áudios ou fotos sem autorização. O repositório ser público não constitui licença de uso do material: nenhuma licença aberta foi escolhida pelo autor até o momento. Materiais curriculares integrais não são redistribuídos aqui.
