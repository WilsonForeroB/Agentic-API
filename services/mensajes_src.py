from fastapi import HTTPException
import asyncio
import logging
from services.agents_service import army_agents
from fastapi.responses import StreamingResponse

# Definición de la cola de mensajes global
message_queue = asyncio.Queue()

# Almacenar sesiones activas
currentSession = []

async def send_message_worker(data, stop_event):
    try:
        message = data.get('message', '')
        if not message:
            raise HTTPException(status_code=400, detail="No se recibió ningún mensaje.")
        
        origen_llamada = data.get("origen_peticion")
        if origen_llamada == 'postman':
            print('PETICION POSTMAN')
            await message_queue.put(StreamingResponse(army_agents(data, stop_event), 
                    media_type="application/x-ndjson", 
                    headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",}
                )
            )
        else:
        # Se coloca la respuesta en la cola para procesarla más adelante
            await message_queue.put(StreamingResponse(army_agents(data, stop_event), media_type="text/event-stream"))
    except Exception as e:
        logging.error(f"Error en send_message_worker: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hubo un error: {str(e)}")

async def stop_generation(user_id, conversation_id):
    try:
        # Buscar si existe la sesión de usuario y conversación
        session = next((element for element in currentSession if element["user_id"] == user_id and element["conversation_id"] == conversation_id), None)
        if session:
            session["stop_event"].set()  # Detener la generación de mensajes
            return {"status": "Proceso detenido"}
        else:
            raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    except Exception as e:
        logging.error(f"Error al detener la generación: {str(e)}")
        raise HTTPException(status_code=500, detail="Hubo un error al detener el proceso.")

async def create_new_session(user_id, conversation_id):
    # Verificar si la sesión ya existe
    session = next((element for element in currentSession if element["user_id"] == user_id and element["conversation_id"] == conversation_id), None)
    if not session:
        # Si no existe, crear una nueva sesión
        session = {"user_id": user_id, "conversation_id": conversation_id, "stop_event": asyncio.Event()}
        currentSession.append(session)
    return session
