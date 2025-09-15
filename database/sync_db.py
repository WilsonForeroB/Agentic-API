from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import variables as var
from sqlalchemy.ext.declarative import declarative_base

# Conexiones a distintas bases
DATABASE_URL = f"postgresql://{var.BD_USUARIO}:{var.BD_CONTRASENA}@{var.BD_HOST}:{var.BD_PUERTO}/{var.BD_BASE_DATOS}"

# Engines
engine_meta = create_engine(DATABASE_URL)

# Session factories
SessionLocalMeta = sessionmaker(autocommit=False, autoflush=False, bind=engine_meta)

BaseMeta = declarative_base()

# Dependencias o métodos para obtener una sesión de cada base
def get_session_meta():
    db = SessionLocalMeta()
    try:
        yield db
    finally:
        db.close()
