from fastapi import APIRouter, HTTPException, Request
from services import mensajes_src
from routes.schemas import MessageRequest, StopRequest, MessageResponse

router = APIRouter(
    prefix="/api/messages",
    tags=["Messages"]
)

@router.post(
    "/send_message",
    response_model=MessageResponse,
    summary="Enviar mensaje",
    description="Envía un mensaje en una conversación, procesado por el worker y devuelve la respuesta generada."
)
async def send_message(request: Request):
    """
    Envía un mensaje de un usuario a una conversación.

    - **user_id**: Identificador del usuario
    - **conversation_id**: Identificador de la conversación
    - **content**: Contenido del mensaje
    """
    data = await request.json()
    headers = request.headers
    data["origen_peticion"] = headers.get('x-origin-api', None)
    session = await mensajes_src.create_new_session(data.get("user_id"), data.get("conversation_id"))
    session["stop_event"].clear()

    await mensajes_src.send_message_worker(data, session["stop_event"])
    result_message = await mensajes_src.message_queue.get()

    return result_message


@router.post(
    "/stop_generation",
    summary="Detener generación de mensajes",
    description="Detiene el proceso de generación en curso para una conversación específica."
)
async def stop_generating(payload: StopRequest):
    """
    Detiene la generación de mensajes para una sesión activa.

    - **user_id**: Identificador del usuario
    - **conversation_id**: Identificador de la conversación
    """
    result = await mensajes_src.stop_generation(payload.user_id, payload.conversation_id)
    return result
