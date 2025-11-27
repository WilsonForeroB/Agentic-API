from models.usuarios import User
from models.roles import Roles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload, selectinload
from typing import Optional, List
from datetime import datetime

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_username(self, user_name: str):
        result = await self.session.execute(select(User).where(User.user_name == user_name))
        return result.scalar_one_or_none()
