from fastapi import FastAPI, APIRouter, Depends, Request
from services.autentificacion_servicio import AuthService
from repositories.user_repositorio import UserRepository
from database.async_db import get_asyn_session_meta
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth Queries"]
)

class LoginRequest(BaseModel):
    user_name: str
    password: str


@router.post("/login")
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_asyn_session_meta)
):
    service = AuthService(UserRepository(db))
    return await service.authenticate_user(credentials.user_name, credentials.password)