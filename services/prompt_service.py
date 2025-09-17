from typing import List, Dict
import asyncio

async def construir_prompt(
    rol: str,
    contexto: str,
    mensaje_usuario: str
) -> List[Dict[str, str]]:
    """
    Construye un prompt para ChatGPT basado en rol, contexto y mensaje del usuario.

    :param rol: El rol o personalidad del asistente (ej: "Eres un profesor de matemáticas.").
    :param contexto: Información de fondo relevante (ej: "El usuario está aprendiendo álgebra.").
    :param mensaje_usuario: Lo que el usuario escribió o preguntó.
    :return: Lista de mensajes en el formato esperado por la API de OpenAI.
    """
    return [
        {"role": "system", "content": rol or "Eres un asistente útil y claro."},
        {"role": "user", "content": f"Contexto: {contexto or 'Sin contexto adicional'}"},
        {"role": "user", "content": mensaje_usuario}
    ]


