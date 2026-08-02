from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks
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

print("\nQuestion:")
print(question)

print("\nRetrieved Documents:")

for i, result in enumerate(results, start=1):
    print("\n-----------------------------")
    print("Result:", i)
    print("Source:", result["source"])
    print("Page:", result["page"])
    print("Distance:", result["distance"])
    print("Text:", result["text"])