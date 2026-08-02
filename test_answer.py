from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks, build_context, generate_answer
from vector_store import create_vector_store, retrieve_documents


pdf_path = "documents/Company_Policy.pdf"

# 1. Extract PDF text
documents = extract_text_from_pdf(pdf_path)

# 2. Create chunks
chunks = create_chunks(documents)

# 3. Create FAISS vector store
index, stored_chunks = create_vector_store(chunks)

# 4. Ask question
question = "How many days of annual leave are employees entitled to?"

# 5. Retrieve relevant chunks
results = retrieve_documents(
    question,
    index,
    stored_chunks,
    top_k=3
)

# 6. Generate answer
answer = generate_answer(question, results)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)