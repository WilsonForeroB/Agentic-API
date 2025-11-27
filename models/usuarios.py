from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, CHAR
)
from sqlalchemy.orm import relationship

from database.sync_db import BaseMeta as Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(255), nullable=False)
    user_name = Column(String(255))
    blocked = Column(Boolean, nullable=False, default=False)
    firstname = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    expiration_password = Column(DateTime)
   
    #user_authentications = relationship("UserAuthentication", back_populates="user", cascade="all, delete-orphan")
    #users_roles = relationship("UsersRoles", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
