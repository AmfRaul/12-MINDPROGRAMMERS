# FieldReach

FieldReach e uma aplicacao web em Django para conectar produtores rurais e compradores. O MVP permite que produtores cadastrem produtos, recebam pedidos e aceitem ou recusem compras. Compradores podem navegar pelo marketplace, fazer pedidos e avaliar compras concluidas.

## Video de pitch + pdf de apresentação

https://drive.google.com/drive/folders/1SYM9RGlC29ABjtBeEab4yIcAwJ-UJXOo

## Funcionalidades

- Cadastro e login de usuarios.
- Dois tipos de conta: produtor e comprador.
- Perfil do produtor com dados comerciais.
- Marketplace com listagem, filtros e detalhe de produtos.
- Cadastro, edicao, exclusao e gestao de produtos pelo produtor.
- Pedido de compra feito pelo comprador.
- Aceite ou recusa do pedido pelo produtor.
- Conclusao de pedido aceito.
- Avaliacao de pedido concluido pelo comprador.
- Dashboard responsivo por perfil de usuario.
- Front-end com Bootstrap 5 e CSS customizado.
- Script `populate.py` para criar dados de teste.

## Tecnologias

- Python
- Django
- SQLite para desenvolvimento local
- Bootstrap 5
- Bootstrap Icons
- Pillow
- python-decouple

## Estrutura principal

```text
accounts/      Usuarios, cadastro, login e perfil da conta
produtores/    Perfil comercial do produtor rural
marketplace/   Categorias, produtos, listagem e gestao de produtos
pedidos/       Pedidos de compra e decisoes do produtor
avaliacoes/    Avaliacoes de pedidos concluidos
dashboard/     Home e painel inicial por tipo de usuario
templates/     Templates HTML da aplicacao
static/        CSS e arquivos estaticos
populate.py    Script para popular o banco com dados de teste
```

## Como rodar localmente

Crie e ative o ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\activate
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Crie um arquivo `.env` com base no `.env.example`:

```text
FIELDREACH_SECRET_KEY=sua-chave-local
FIELDREACH_DEBUG=True
FIELDREACH_ALLOWED_HOSTS=localhost,127.0.0.1
```

Aplique as migracoes:

```powershell
python manage.py migrate
```

Popule o banco com dados de teste:

```powershell
python populate.py
```

Inicie o servidor:

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Usuarios de teste

A senha de todos os usuarios criados pelo `populate.py` e:

```text
senha12345
```

Produtores:

```text
joao_produtor
maria_produtora
```

Compradores:

```text
ana_compradora
bruno_comprador
```

Admin:

```text
admin
```

## Fluxo do MVP

1. O produtor entra na plataforma.
2. Completa o perfil de produtor.
3. Cadastra produtos no marketplace.
4. O comprador acessa o marketplace e faz um pedido.
5. O produtor aceita ou recusa o pedido.
6. Se aceito, o produtor pode marcar o pedido como concluido.
7. O comprador avalia o pedido concluido.

## Testes

Execute:

```powershell
python manage.py test
```

Tambem e recomendado rodar:

```powershell
python manage.py check
```

## Observacoes para deploy

Para testes, o projeto pode rodar com SQLite. Para um MVP publico, o ideal e configurar PostgreSQL, `DEBUG=False`, `ALLOWED_HOSTS` do dominio do deploy e servir arquivos estaticos corretamente.
