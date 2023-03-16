# Trilha NADIC - Back-end

## Projetos

### Projeto 1: Git e Github

- Esse repositório foi criado usando o git integrado com o gitflow.
- O gitflow foi utilizado para gerar a branch de developmentm, além de criar as branches de feature (recursos e funcionalidades) e de release (lançamento e versão).
- Foram usados comandos como `git flow init`; `git flow feature init ...` ; `git flow release start ...`; Entre outros.

### Projeto 2: MySQL

- Foi criado um banco de dados MySQL com uma tabela de livros e uma tabela de categorias.
- A tabela de livros tem relacionamento `1 para N` com a tabela de categorias.`
- Foram inseridos, atualizados e deletados dados nas 2 tabelas.
- Foi feito um `JOIN` entre as tabelas para mostrar os livros e suas categorias.
- Foi feito um `GROUP BY` junto com um `COUNT()` para mostrar a quantidade de livros por categoria.

### Projeto 3: Django

- Foi criado um projeto Django para simular uma empresa de venda de livros online.
- Cada vendedor da empresa tem uma conta que é usada para fazer login no sistema.
- A conta é criada pelo `superuser` do django
- O vendedor pode adicionar livros, editar e remover livros. Além de aumentar o estoque de um produto e vendê-los, diminuindo o estoque.
- O vendedor pode ver o histórico de vendas geral e o pessoal dele.
- Foram adicionados testes unitários para todas as urls e views do projeto.

#### Como rodar o projeto

- Clone o repositório
- Crie um ambiente virtual: `python -m venv .venv` (Windows) ou `python3 -m venv .venv` (Linux)
- Instale as dependências: `pip install -r requirements.txt`
- Rode as migrações: `.\manage.py migrate`
- Crie um superuser: `.\manage.py createsuperuser`
- Com o ambiente aberto, rode o servidor: `.\manage.py runserver`

### Projeto 4: Django Rest Framework

- Feature do projeto 3
- Foi criado uma API Rest com a biblioteca django-rest-framework para o projeto 4
- A API tem endpoints para listar, criar, editar e deletar (CRUD) livros, vendas e usuários.
- A API tem um sistema de autenticação com token JWT.
- A API tem um sistema de permissões para os usuários, sendo alguns endpoints permitidos apenas para o admin (superuser do django).
- Além dos CRUDs, a API tem endpoints para mostrar o histórico de vendas de um usuário específico e para visualizar o faturamento total da empresa (apenas admin).
- Foram adicionados testes unitários para todas as viewsets do projeto.

#### Regras de negócio

- Para criar um usuário, não é necessário estar logado.
- Para o CRUD de livros e de vendas, é necessário estar logado.
- Para visualizar o faturamento total da empresa, é necessário ser admin.
