from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks


pdf_path = "documents/Company_Policy.pdf"

documents = extract_text_from_pdf(pdf_path)

chunks = create_chunks(documents)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print("\n-----------------------------")
    print("Chunk:", i)
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"])