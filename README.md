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

# Ruff

`poetry add --group dev ruff`

# Pytest

`poetry add --group dev pytest pytest-cov`

# Taskipy

`poetry add --group dev taskipy`