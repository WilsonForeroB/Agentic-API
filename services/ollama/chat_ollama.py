import requests

# ===============================
# CONFIG
# ===============================
MODEL = "llama3.2:1b"   # 👈 cambia el modelo aquí
API_URL = "http://localhost:11434/api/chat"

# ===============================
# OLLAMA CHAT CALL
# ===============================
def ollama_chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"🔥 Error Ollama: {response.text}")

    data = response.json()
    return data["message"]["content"]

# ===============================
# MAIN LOOP
# ===============================
if __name__ == "__main__":
    print("💬 Chat con Ollama")
    print("Escribe 'exit' para salir\n")

    messages = [
        {"role": "system", "content": "Eres un asistente útil y conciso."}
    ]

    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Saliendo...")
            break

        messages.append({"role": "user", "content": user_input})

        respuesta = ollama_chat(messages)

        print(f"\n🤖 Ollama: {respuesta}\n")

        messages.append({"role": "assistant", "content": respuesta})
