import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


model = load_embedding_model()


# ============================================================
# CREATE VECTOR STORE
# ============================================================

def create_vector_store(chunks):
    """
    Create a FAISS vector store from document chunks.

    Returns:
        FAISS index
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    ).astype("float32")

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)

    return index


# ============================================================
# SEARCH VECTOR STORE
# ============================================================

def search_vector_store(
    index,
    chunks,
    query,
    k=3
):
    """
    Search the FAISS vector store and return
    the most relevant document chunks.
    """

    if index is None:
        return []

    if not chunks:
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        show_progress_bar=False
    ).astype("float32")

    # Never request more results than available chunks
    k = min(k, len(chunks))

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if (
            idx != -1
            and idx < len(chunks)
        ):

            result = chunks[idx].copy()

            result["distance"] = float(distance)

            results.append(result)

    return results