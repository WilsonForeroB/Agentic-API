from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from database.sync_db import BaseMeta as Base

class MasterPrompts(Base):
    __tablename__ = 'maestro_prompts'

    prompt_id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_internal_name = Column(String(255), nullable=True, unique=True)
    prompt_description = Column(Text, nullable=True)
    prompt_content = Column(Text, nullable=False)
    creation_date = Column(DateTime, default=func.now(), nullable=True)
    active = Column(Boolean, default=False)