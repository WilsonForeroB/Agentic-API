0. Se debe crear una base de datos en postgres con nombre Agentic_DB
Para implementar la base de datos ejecutar desde la raiz del proyecto:
1. alembic init migrations
Luego:
2. alembic -c migrations/alembic.ini revision --autogenerate -m "MENSAJE"
Esto genera la estructura en la base de datos que esta configurada:
3. alembic -c migrations/alembic.ini upgrade head