from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    Keeps the document name and page number as metadata.
    """

    reader = PdfReader(pdf_path)
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append({
                "text": text.strip(),
                "source": pdf_path,
                "page": page_number
            })

    return documents