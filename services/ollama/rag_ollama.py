##############################################
#      DEMO RAG con OLLAMA embeddings vía API
#  (modelo: nomic-embed-text)
##############################################

import requests
import math

TXT_FILE = "utils/textos_rag/clima.txt"
CHUNK_SIZE = 300
MODEL = "nomic-embed-text:latest"
API_URL = "http://localhost:11434/api/embed"


# ==============================================================
# OLLAMA API CALL
# ==============================================================
def ollama_embed(text):
    """
    Genera embeddings usando la API HTTP de Ollama.
    Retorna un vector (lista de floats).
    """
    payload = {
        "model": MODEL,
        "input": text
    }
    response = requests.post(API_URL, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"🔥 Error en Ollama API: {response.text}")

    data = response.json()
    return data["embeddings"][0]


# ==============================================================
# UTILIDADES
# ==============================================================
def cargar_texto(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def hacer_chunks(texto, tamaño):
    return [texto[i:i+tamaño] for i in range(0, len(texto), tamaño)]


def mostrar_chunks(chunks, embeddings):
    for i, c in enumerate(chunks):
        print(f"\n--- CHUNK {i} ---")
        print(c)
        print("\nVector (primeros 5 valores): ")
        print(embeddings[i][:5])


def cos_sim(v1, v2):
    """
    Similaridad coseno entre vectores
    """
    dot = sum(a*b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a*a for a in v1))
    norm2 = math.sqrt(sum(b*b for b in v2))
    return dot / (norm1 * norm2)


# ==============================================================
# BUSQUEDA SEMANTICA
# ==============================================================
def buscar_semantica(query, embeddings, chunks, threshold=0.5):
    qvec = ollama_embed(query)
    resultados = []

    for i, emb in enumerate(embeddings):
        sim = cos_sim(qvec, emb)
        if sim >= threshold:
            resultados.append((i, sim, chunks[i]))

    return sorted(resultados, key=lambda x: x[1], reverse=True)


# ==============================================================
# MAIN
# ==============================================================
if __name__ == "__main__":
    print("📄 Cargando archivo...")
    texto = cargar_texto(TXT_FILE)

    print("🧩 Dividiendo en chunks...")
    chunks = hacer_chunks(texto, CHUNK_SIZE)
    print(f"🔢 Total de fragmentos: {len(chunks)}")

    print("🧠 Generando embeddings con Ollama...")
    embeddings = [ollama_embed(chunk) for chunk in chunks]

    ver = input("\n¿Mostrar chunks + vector? (s/n): ")
    if ver.lower() == "s":
        mostrar_chunks(chunks, embeddings)

    query = input("\n👉 Ingresa tu consulta semántica: ")

    resultados = buscar_semantica(query, embeddings, chunks, threshold=0.5)

    print("\n====== RESULTADOS ≥ 0.5 ======")
    if not resultados:
        print("⚠️ No se encontraron coincidencias")
    else:
        for idx, sim, texto in resultados:
            print(f"\n📌 CHUNK {idx} — Similitud: {sim:.3f}")
            print(texto)
            print("------")
