import asyncio
import random
from services.maestrodb_service import DBService
from database.async_db import get_asyn_session_meta

async def army_agents(datausuario, stop_event=0):

    async for session in get_asyn_session_meta():
        db = DBService(session)
        agentes = await db.obtener_agentes()
        print(agentes)

    for _ in range(5):
        # Genera un número aleatorio
        numero = random.randint(1, 100)
        # Envía el número como texto (puedes enviarlo en JSON si prefieres)
        yield f"{numero}\n".encode()
        # Simula un pequeño retardo entre envíos
        await asyncio.sleep(1)