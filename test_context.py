from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks, build_context
from vector_store import create_vector_store, retrieve_documents


pdf_path = "documents/Company_Policy.pdf"

documents = extract_text_from_pdf(pdf_path)

chunks = create_chunks(documents)

index, stored_chunks = create_vector_store(chunks)

question = "How many days of annual leave are employees entitled to?"

results = retrieve_documents(
    question,
    index,
    stored_chunks,
    top_k=3
)

context = build_context(results)

print("\nQUESTION:")
print(question)

print("\nRETRIEVED CONTEXT:")
print(context)