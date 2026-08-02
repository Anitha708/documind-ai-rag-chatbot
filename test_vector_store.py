from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks
from vector_store import create_vector_store


pdf_path = "documents/Company_Policy.pdf"

documents = extract_text_from_pdf(pdf_path)

chunks = create_chunks(documents)

index, stored_chunks = create_vector_store(chunks)

print("Number of chunks:", len(stored_chunks))
print("FAISS index size:", index.ntotal)
print("Embedding dimension:", index.d)