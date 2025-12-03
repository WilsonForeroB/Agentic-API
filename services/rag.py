from sentence_transformers import SentenceTransformer, util

# ---------- Configuración ----------
TXT_FILE = "utils/textos_rag/noticias.txt"     # Cambia el archivo si quieres
CHUNK_SIZE = 300                # Nº de caracteres por fragmento
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def cargar_texto(path):
    """Lee un archivo .txt y devuelve un string"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def hacer_chunks(texto, tamaño):
    """Divide el texto en fragmentos tipo sliding window"""
    return [texto[i:i+tamaño] for i in range(0, len(texto), tamaño)]

def mostrar_chunks(chunks, embeddings):
    """Imprime cada chunk y su vector asociado"""
    for i, c in enumerate(chunks):
        print(f"\n--- CHUNK {i} ---")
        print(c)
        print("\nVector (primeros 5 valores): ")
        print(embeddings[i][:5])  # Para no imprimir todo el vector

def buscar_semantica(query, embeddings, chunks, threshold=0.5):
    """Realiza búsqueda semántica y devuelve chunks relevantes"""
    query_embed = model.encode(query, convert_to_tensor=True)
    similitudes = util.cos_sim(query_embed, embeddings)[0]

    resultados = []
    for i, sim in enumerate(similitudes):
        if sim >= threshold:
            resultados.append((i, float(sim), chunks[i]))
    return resultados

# ---------------- MAIN ----------------
if __name__ == "__main__":
    ### siempre se hace en el backend ##
    print("Cargando modelo embeddings...")
    model = SentenceTransformer(MODEL_NAME)

    print("Leyendo archivo...")
    texto = cargar_texto(TXT_FILE)

    print("Dividiendo texto en chunks...")
    chunks = hacer_chunks(texto, CHUNK_SIZE)

    print(f"Total de fragmentos generados: {len(chunks)}")

    # Creamos embeddings para cada chunk
    print("Generando embeddings...")
    embeddings = model.encode(chunks, convert_to_tensor=True)

    # Mostrar chunks y vectores
    ver = input("\n¿Deseas imprimir chunks y vectores? (s/n): ")
    if ver.lower() == "s":
        mostrar_chunks(chunks, embeddings)
    ### siempre se hace en el backend ##

    #llamado de tu API ##
    # Pregunta del usuario
    query = input("\n👉 Escribe tu consulta semántica: ")

    resultados = buscar_semantica(query, embeddings, chunks, threshold=0.5)

    #RESULTADO DEL A BUSQUEDA EN LA BASE DE DATOS VECTORIAL ##
    print("\n====== RESULTADOS (similitud ≥ 50%) ======")
    if not resultados:
        print("⚠️ No se encontraron coincidencias.")
    else:
        for idx, sim, texto in resultados:
            print(f"\n📌 CHUNK {idx} — Similitud: {sim:.2f}")
            print(texto)

    #PASAR LA RESPUESTA A UN LLM ##

    # ENVIAR LA RESPUESTA AL CLIENTE
