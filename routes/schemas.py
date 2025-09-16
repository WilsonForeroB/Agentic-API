from pydantic import BaseModel
from typing import Any, Dict

class MessageRequest(BaseModel):
    user_id: int
    conversation_id: str
    message: str

class StopRequest(BaseModel):
    user_id: str
    conversation_id: str

class MessageResponse(BaseModel):
    message: Dict[str, Any]  # Ajusta según lo que devuelva mensajes_src