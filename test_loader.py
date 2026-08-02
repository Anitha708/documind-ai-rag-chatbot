from document_loader import extract_text_from_pdf

pdf_path = "documents/Company_Policy.pdf"

documents = extract_text_from_pdf(pdf_path)

print(f"Pages with text found: {len(documents)}")

for document in documents:
    print("\n-----------------------------")
    print("Source:", document["source"])
    print("Page:", document["page"])
    print("Text:", document["text"][:300])