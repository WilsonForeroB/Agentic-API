import asyncio
import random
from services.maestrodb_service import DBService
from database.async_db import get_asyn_session_meta
from services.prompt_service import construir_prompt
from services.openai.stream_call import obtener_respuesta_stream_openai
from services.openai.normal_call import obtener_respuesta_openai

import json

async def army_agents(datausuario, stop_event=0):

    lista_variables = {} # aqui deberia tener las variables asociadas a la sesion del usuario.

    async for session in get_asyn_session_meta():
        db = DBService(session)
        agentes = await db.obtener_agentes()
        print('Agentes', agentes)

    rol_agente = await decisor_agente(datausuario, agentes, lista_variables)
    print('Rol agente decisor:', rol_agente)

    prompt = await construir_prompt(
        rol=rol_agente, # aqui deberia ir el prompt del agente
        contexto="El usuario esta en un curso de AI.", # deberia ir el historial del chat
        mensaje_usuario=datausuario.get('message', 'Sin información')
    )


    async for frag in obtener_respuesta_stream_openai(prompt, lista_variables):
        try:
            json.loads(frag)  # intenta parsear
            # Si es JSON válido, no se envía y se deberia almacenar en una tabla de log.
            continue
        except json.JSONDecodeError:
            # Si NO es JSON válido, lo enviamos
            yield frag


async def decisor_agente(datausuario, datos_decidir, lista_variables):
    # Prompt genérico de respaldo (esto deberia venir por un maestro prompt generico)
    prompt_generico = (
        "Soy un asistente general que puede ayudarte a resolver dudas, "
        "responder preguntas y guiarte en lo que necesites."
    )

    # Construimos el contexto con ids y descripciones
    stream_context = "\n".join(
        f"{a['agent_id']}, {a['agent_description']}" for a in datos_decidir
    )

    # Prompt dinámico para que OpenAI decida
    prompt = await construir_prompt(
        rol="Tu función es decidir cuál es el mejor agente para responder la solicitud del cliente. "
            "Únicamente responde con el número del agent_id",
        contexto=stream_context,
        mensaje_usuario=datausuario.get('message', 'Sin información')
    )

    # Llamada al modelo
    respuesta = await obtener_respuesta_openai(prompt, {})
    
    agente_resp = respuesta["choices"][0]["message"]["content"]

    # Normalizamos la respuesta
    try:
        agente_id = int(str(agente_resp).strip())
    except (ValueError, AttributeError):
        return prompt_generico  # fallback inmediato

    # Buscamos el agent_prompt correspondiente
    for agente in datos_decidir:
        if agente["agent_id"] == agente_id:
            return agente["agent_prompt"]

    # Si no se encontró el agent_id, devolvemos el prompt genérico
    return prompt_generico




