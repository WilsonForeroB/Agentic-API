from sqlalchemy import pool
from alembic import context
import sys
import os

# Agregar la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from database.sync_db import BaseMeta, engine_meta
from models import (
    agentes,
    maestro_prompts
        )

config = context.config

if config.config_file_name is not None:
    from logging.config import fileConfig
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = BaseMeta.metadata

def run_migrations_offline():
    """Configuración para modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, 
        target_metadata=target_metadata, 
        literal_binds=True, 
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Configuración para modo 'online'."""
    connectable = engine_meta  # Usamos el engine importado directamente

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
