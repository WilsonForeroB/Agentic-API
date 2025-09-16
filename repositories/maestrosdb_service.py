from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from models.agentes import Agent
from models.maestro_prompts import MasterPrompts
from utils.helpers import orm_to_dict

class DBRepository:
    def __init__(self, session):
        self.session = session

    async def agentes_obtener_todos(self):
        stmt = select(Agent).where(Agent.active_agent == True).order_by(Agent.agent_name)
        result = await self.session.execute(stmt)
        agentes = result.scalars().all()
        return orm_to_dict(agentes)
    
    async def prompts_obtener_todos(self):
        stmt = select(MasterPrompts).where(MasterPrompts.active == True)
        result = await self.session.execute(stmt)
        agentes = result.scalars().all()
        return agentes