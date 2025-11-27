from passlib.context import CryptContext
from repositories.user_repositorio import UserRepository
from utils.token import create_access_token
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import random, string
import requests
import json
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import asyncio
import logging
import time
import http.client
import httpx
import xml.etree.ElementTree as ET

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],  # soporta ambos
    default="pbkdf2_sha256",              # nuevo estándar
    deprecated="auto"                     # marca bcrypt como obsoleto
)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, user_name: str, password: str):

        usuario = await self.user_repository.get_by_username(user_name)
        token = ''

        if not usuario:

            return {"token": token, "acceso": False}
        
        # metodo de validación de contraseña

        token = create_access_token(data={"usr": user_name, "otros": "agregar informacion api"})
        
        return {"token": token, "acceso": True}