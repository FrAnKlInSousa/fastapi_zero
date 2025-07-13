# PIPX

`sudo apt install pipx`
`pipx ensurepath`

# Poetry

`pipx install poetry`
`pipx inject poetry poetry-plugin-shell`

Na pasta onde será criado o projeto (a tag flat serve para deixar o projeto sem a pasta src):

`poetry --flat new fastapi_zero`

# Python
Na pasta do projeto:

`poetry python install 3.13`
`poetry env use 3.13`

# FastAPI

`poetry add fastapi[standard]`

# Ambiente virtual

## Ativando

`poetry shell`

se, ao usar o comando `fastapi`, não reconhecer, tente as seguintes abordagens:

`pipx inject poetry poetry-plugin-shell --force`

`poetry self add poetry-plugin-shell`

# Executando o projeto

`fastapi dev fastapi_zero/app.py`
ou se não reconhecer o ambiente virtual:
`poetry run fastapi dev fastapi_zero/app.py`

# Libs
## Ruff

`poetry add --group dev ruff`

## Pytest

`poetry add --group dev pytest pytest-cov`

## Taskipy

`poetry add --group dev taskipy`

## SQLAlchemy

`poetry add sqlalchemy`

## Pydantic-settings

`poetry add pydantic-settings`

## Alembic

`poetry add alembic`
### Comandos principais
* inicia um sistema de migração:
`alembic init migrations`
* cria uma migração:
`alembic revision --autogenerate -m "create users table"`
* aplica uma migração:
`alembic upgrade head`

# PWDlib
`poetry add "pwdlib[argon2]"`

# PyJWT
`poetry add pyjwt`

# tzdata
* Dependendo da compilação do python, as propriedades do timezone 
* podem não estar disponíveis. Para resolver isso, basta instalar o tzdata:
`poetry add tzdata`

# Database
## SQLite
* Para conectar pelo terminal:
`python -m sqlite3 database.db`
* ou para ter uma visualização diferente do banco:
`pipx run harlequin database.db`

# Secret Key

* Uma forma de gerar uma secret key com o python:
```python
import secrets

secrets.token_hex(256)
```
