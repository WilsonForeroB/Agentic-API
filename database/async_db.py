from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import variables as var

# Conexiones a distintas bases
DATABASE_URL = f"postgresql+asyncpg://{var.BD_USUARIO}:{var.BD_CONTRASENA}@{var.BD_HOST}:{var.BD_PUERTO}/{var.BD_BASE_DATOS}"

# Engines
async_engine_meta = create_async_engine(DATABASE_URL, echo=False)

# Session factories
AsyncSessionLocalMeta = sessionmaker(
    bind=async_engine_meta,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Declarative Base
AsynBaseMeta = declarative_base()

# Dependencias o métodos para obtener una sesión de cada base
async def get_asyn_session_meta():
    async with AsyncSessionLocalMeta() as session:
        yield session
