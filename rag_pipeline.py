# ============================================================
# RAG PIPELINE
# ============================================================

from typing import List, Dict


# ============================================================
# CREATE TEXT CHUNKS
# ============================================================

def create_chunks(
    documents: List[Dict],
    chunk_size: int = 800,
    overlap: int = 150
) -> List[Dict]:

    chunks = []

    if not documents:
        return chunks

    for document in documents:

        text = document.get("text", "").strip()

        if not text:
            continue

        source = document.get("source", "Unknown")
        page = document.get("page", "N/A")

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append(
                    {
                        "text": chunk_text,
                        "source": source,
                        "page": page
                    }
                )

            if end >= len(text):
                break

            start = end - overlap

    return chunks


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question: str,
    retrieved_documents: List[Dict]
) -> str:

    if not retrieved_documents:

        return (
            "I could not find relevant information in "
            "the uploaded documents."
        )

    # --------------------------------------------------------
    # Build context from retrieved chunks
    # --------------------------------------------------------

    context_parts = []

    for document in retrieved_documents:

        text = document.get("text", "").strip()

        if text:
            context_parts.append(text)

    context = "\n\n".join(context_parts)

    if not context:

        return (
            "I could not find enough information in "
            "the uploaded documents to answer this question."
        )

    # --------------------------------------------------------
    # Try Google Gemini if configured
    # --------------------------------------------------------

    try:

        import os

        api_key = os.getenv("GOOGLE_API_KEY")

        if api_key:

            from google import genai

            client = genai.Client(
                api_key=api_key
            )

            prompt = f"""
You are DocuMind AI, a document question-answering assistant.

Answer the user's question ONLY using the supplied document
context.

If the answer cannot be found in the context, say:

"I couldn't find that information in the uploaded documents."

Do not invent facts.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

Give a clear and concise answer.
"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            if response and response.text:

                return response.text.strip()

    except Exception:
        pass

    # --------------------------------------------------------
    # Fallback answer
    # --------------------------------------------------------

    return (
        "I found the following relevant information in your "
        "uploaded document:\n\n"
        + context[:3000]
    )