from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, CHAR
)
from sqlalchemy.orm import relationship
from database.sync_db import BaseMeta as Base

class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    rol = Column(String(155))
    created_at = Column(DateTime)
    created_by = Column(String(155))
    updated_at = Column(DateTime)
    updated_by = Column(String(155))

    #users_roles = relationship("UsersRoles", back_populates="role", cascade="all, delete-orphan", passive_deletes=True)
    #roles_permisos = relationship("RolesPermisos", back_populates="role", cascade="all, delete-orphan", passive_deletes=True)