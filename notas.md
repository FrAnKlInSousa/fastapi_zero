configs feitas durante o curso, mas que foram substituídas:
DATABASE_URL="sqlite:///database.db" versao sem async
DATABASE_URL="sqlite+aiosqlite:///database.db"
DATABASE_URL="{banco}://{user}:{password}@{host}:{port}/{db_name}"

docker run --name app_database -e POSTGRES_USER=app_user -e POSTGRES_DB=app_db -e POSTGRES_PASSWORD=app_password -p 5432:5432 postgres
# Docker compose
* se for requisitada permissão para rodar o arquivo .entrypoint.sh:
* `chmod +x entrypoint.sh`