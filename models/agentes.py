from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from database.sync_db import BaseMeta as Base
from sqlalchemy.orm import relationship

class Agent(Base):
    __tablename__ = 'agents'

    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    agent_name = Column(String(255), nullable=False)
    agent_prompt = Column(Text, nullable=False)
    agent_description = Column(Text, nullable=True)  
    creation_date = Column(DateTime, default=func.now(), nullable=False)
    active_agent = Column(Boolean, nullable=True, default=True)

    