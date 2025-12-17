import requests
import gradio as gr
import math

# ===============================
# CONFIG
# ===============================
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:1b"

EMBED_URL = "http://localhost:11434/api/embed"
CHAT_URL = "http://localhost:11434/v1/chat/completions"

CHUNK_SIZE = 300

# ===============================
# OLLAMA API
# ===============================
def ollama_embed(text):
    payload = {"model": EMBED_MODEL, "input": text}
    r = requests.post(EMBED_URL, json=payload)
    r.raise_for_status()
    return r.json()["embeddings"][0]

def ollama_chat(messages):
    clean_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if "role" in m and "content" in m
    ]

    payload = {
        "model": CHAT_MODEL,
        "messages": clean_messages,
        "stream": False
    }

    r = requests.post(CHAT_URL, json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ===============================
# UTILIDADES RAG
# ===============================
def hacer_chunks(texto, tamaño):
    return [texto[i:i+tamaño] for i in range(0, len(texto), tamaño)]

def cos_sim(v1, v2):
    dot = sum(a*b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a*a for a in v1))
    n2 = math.sqrt(sum(b*b for b in v2))
    return dot / (n1 * n2)

def buscar_semantica(query, embeddings, chunks, threshold=0.4):
    qvec = ollama_embed(query)
    results = []

    for i, emb in enumerate(embeddings):
        sim = cos_sim(qvec, emb)
        if sim >= threshold:
            results.append((i, sim, chunks[i]))

    return sorted(results, key=lambda x: x[1], reverse=True)

# ===============================
# TAB 1: EMBEDDINGS
# ===============================
def generar_embeddings(texto):
    if not texto.strip():
        return [], [], "❌ Texto vacío"

    chunks = hacer_chunks(texto, CHUNK_SIZE)
    embeddings = [ollama_embed(c) for c in chunks]

    return chunks, embeddings, f"✅ {len(chunks)} chunks generados"

def consulta_semantica(query, chunks, embeddings):
    if not query.strip():
        return "❌ Consulta vacía"

    results = buscar_semantica(query, embeddings, chunks)
    if not results:
        return "⚠️ Sin resultados"

    salida = ""
    for i, sim, txt in results:
        salida += f"🔹 Chunk {i} | Sim: {sim:.3f}\n{txt}\n\n"

    return salida

# ===============================
# TAB 2: CHAT (FIX GRADIO)
# ===============================
def chat_gradio(user_input, messages):
    messages.append({"role": "user", "content": user_input})

    try:
        respuesta = ollama_chat(messages)
    except Exception as e:
        respuesta = f"❌ Error: {e}"

    messages.append({"role": "assistant", "content": respuesta})

    return messages, messages

# ===============================
# UI GRADIO
# ===============================
with gr.Blocks(title="Ollama AI Studio") as demo:
    gr.Markdown("# 🤖 Ollama AI Studio")

    with gr.Tabs():

        # -------- TAB EMBEDDINGS --------
        with gr.Tab("🧠 Embeddings"):
            gr.Markdown("### Búsqueda semántica con Ollama")

            texto_input = gr.Textbox(
                lines=10,
                label="Texto base"
            )

            gen_btn = gr.Button("Generar embeddings")
            status = gr.Markdown()

            chunks_state = gr.State([])
            embeddings_state = gr.State([])

            gen_btn.click(
                generar_embeddings,
                inputs=texto_input,
                outputs=[chunks_state, embeddings_state, status]
            )

            query_input = gr.Textbox(label="Consulta semántica")
            result_box = gr.Textbox(lines=12, label="Resultados")

            query_input.submit(
                consulta_semantica,
                inputs=[query_input, chunks_state, embeddings_state],
                outputs=result_box
            )

        # -------- TAB CHAT --------
        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(height=450)
            input_txt = gr.Textbox(
                placeholder="Escribe tu mensaje...",
                show_label=False
            )

            chat_state = gr.State([
                {"role": "system", "content": "Eres un asistente útil y conciso."}
            ])

            input_txt.submit(
                chat_gradio,
                inputs=[input_txt, chatbot],
                outputs=[chatbot, chat_state]
            )

            input_txt.submit(
                lambda: "",
                None,
                input_txt
            )

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    demo.launch()
