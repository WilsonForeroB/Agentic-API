from repositories.maestrosdb_service import DBRepository

class DBService:
    def __init__(self, session):
        self.session = session
        self.repo = DBRepository(session)

    async def obtener_agentes(self):
        return await self.repo.agentes_obtener_todos()
    
    async def obtener_maestro_prompts(self):
        return await self.repo.prompts_obtener_todos()

