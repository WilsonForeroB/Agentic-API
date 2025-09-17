import aiohttp
import json
import time
import tiktoken
from variables import API_KEY_OPENAI, MODELO_CHATGPT,URL_CHATGPT_COMPLETIONS

encoder = tiktoken.encoding_for_model("gpt-4o")

async def obtener_respuesta_stream_openai(prompt_openai, lista_variables):
    data = {
        "model": MODELO_CHATGPT,
        "messages": prompt_openai,
        "max_tokens": lista_variables.get('MODELO_TOKENS', 1024),
        "top_p": lista_variables.get('top_p', 1.0),
        "temperature": lista_variables.get('MODELO_TEMPERATURA', 0.7),
        "stream": True
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY_OPENAI}"
    }

    tiempo_inicio = time.time()
    respuesta_completa = ""
    respuesta_parcial = ""
    contador_signos = 0
    data_llm = None

    async with aiohttp.ClientSession() as session:
        async with session.post(URL_CHATGPT_COMPLETIONS,
                                data=json.dumps(data), headers=headers) as response:
            if response.status == 200:
                async for line in response.content:
                    decoded_line = line.decode('utf-8').strip()

                    if not decoded_line:
                        continue  # sigue leyendo

                    if decoded_line == "data: [DONE]":
                        # Si quedó algo parcial, lo envío antes de terminar
                        if respuesta_parcial:
                            yield respuesta_parcial
                        break

                    if decoded_line.startswith("data:"):
                        fragmento = decoded_line[5:].strip()
                        if fragmento:
                            data_llm = json.loads(fragmento)
                            delta = data_llm['choices'][0]['delta']

                            if 'content' in delta:
                                choice_text = delta['content']
                                respuesta_completa += choice_text
                                respuesta_parcial += choice_text
                                contador_signos += 1

                                if contador_signos >= 5:
                                    yield respuesta_parcial
                                    respuesta_parcial = ""
                                    contador_signos = 0
            else:
                text = await response.text()
                print(f"Error en la solicitud: {response.status}, {text}")
                yield None
                return

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio

    prompt_text = "\n".join([msg["content"] for msg in prompt_openai])
    tokens_prom = len(encoder.encode(prompt_text))
    tokens_respuesta = len(encoder.encode(respuesta_completa))

    resultado_json = {
        "id": data_llm["id"] if data_llm else None,
        "object": "chat.completion",
        "created": data_llm["created"] if data_llm else None,
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

    resultado_json_str = json.dumps(resultado_json, indent=4)
    yield resultado_json_str
