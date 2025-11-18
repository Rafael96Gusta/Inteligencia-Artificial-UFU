from openai import OpenAI
import numpy as np
import traceback
import asyncio

client = OpenAI()

# Memória
stored_texts: list[str] = []
stored_embeddings: list[list[float]] = []


async def index_texts(texts: list[str]):
    """
    Gera embeddings e armazena para busca posterior.
    Pode ser usada para indexar artigos, capítulos ou resumos.
    """
    global stored_texts, stored_embeddings

    try:
        if not texts:
            raise ValueError("Lista de textos vazia.")

        print(f"🔹 Indexando {len(texts)} textos...")

        response = await asyncio.to_thread(
            client.embeddings.create,
            model="text-embedding-3-small",
            input=texts
        )

        stored_texts = texts
        stored_embeddings = [item.embedding for item in response.data]

        print(f"✅ Indexação concluída com sucesso ({len(stored_embeddings)} embeddings gerados).")

    except Exception as e:
        print("Erro durante indexação:")
        traceback.print_exc()
        raise RuntimeError(f"Erro ao gerar embeddings: {e}")


async def search_similar(query: str, top_k: int = 5):
    """
    Busca textos semelhantes à query com base em embeddings.
    """
    if not stored_embeddings:
        return ["Nenhum texto indexado ainda."]

    try:
        print(f"🔍 Gerando embedding para a consulta: {query[:60]}...")

        query_response = await asyncio.to_thread(
            client.embeddings.create,
            model="text-embedding-3-small",
            input=query
        )
        query_vector = query_response.data[0].embedding

        similarities = [
            np.dot(query_vector, emb) / (np.linalg.norm(query_vector) * np.linalg.norm(emb))
            for emb in stored_embeddings
        ]

        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [stored_texts[i] for i in top_indices]

        print(f"Retornando {len(results)} resultados mais semelhantes.")
        return results

    except Exception as e:
        print("Erro na busca semântica:")
        traceback.print_exc()
        return [f"Erro ao processar busca: {e}"]
