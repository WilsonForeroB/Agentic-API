import aiohttp
import json
import time
import tiktoken
from variables import API_KEY_OPENAI, MODELO_CHATGPT, URL_CHATGPT_COMPLETIONS

encoder = tiktoken.encoding_for_model("gpt-4o")

async def obtener_respuesta_openai(prompt_openai, lista_variables):
    data = {
        "model": MODELO_CHATGPT,
        "messages": prompt_openai,
        "max_tokens": lista_variables.get('MODELO_TOKENS', 1024),
        "top_p": lista_variables.get('top_p', 1.0),
        "temperature": lista_variables.get('MODELO_TEMPERATURA', 0.7),
        "stream": False   # 🚨 clave: desactivar streaming
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY_OPENAI}"
    }

    tiempo_inicio = time.time()
    respuesta_completa = None
    data_llm = None

    async with aiohttp.ClientSession() as session:
        async with session.post(URL_CHATGPT_COMPLETIONS,
                                data=json.dumps(data), headers=headers) as response:
            if response.status == 200:
                data_llm = await response.json()
                respuesta_completa = data_llm["choices"][0]["message"]["content"]
            else:
                text = await response.text()
                print(f"Error en la solicitud: {response.status}, {text}")
                return None

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio

    # Calcular tokens de entrada y salida
    prompt_text = "\n".join([msg["content"] for msg in prompt_openai])
    tokens_prom = len(encoder.encode(prompt_text))
    tokens_respuesta = len(encoder.encode(respuesta_completa)) if respuesta_completa else 0

    resultado_json = {
        "id": data_llm.get("id") if data_llm else None,
        "object": "chat.completion",
        "created": data_llm.get("created") if data_llm else None,
        "model": MODELO_CHATGPT,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": respuesta_completa
                },
                "index": 0,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": tokens_prom,
            "completion_tokens": tokens_respuesta,
            "total_tokens": tokens_prom + tokens_respuesta,
            "tiempo_inicio": tiempo_inicio,
            "tiempo_fin": tiempo_fin,
            "tiempo_total": tiempo_total
        }
    }

    # 🔹 Ahora devuelve directamente el JSON (no hay yield)
    return resultado_json
