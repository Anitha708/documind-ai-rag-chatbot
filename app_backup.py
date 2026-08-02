import streamlit as st
import os
import tempfile

from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks, generate_answer
from vector_store import create_vector_store, search_vector_store


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("📚 Domain-Specific RAG Chatbot")

st.write(
    "Upload PDF documents and ask questions "
    "based on their content."
)


# ==========================================
# SESSION STATE
# ==========================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("📂 Document Upload")


uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


# ==========================================
# PROCESS DOCUMENTS
# ==========================================

if uploaded_files:

    st.sidebar.write("### Uploaded Documents")

    for file in uploaded_files:

        st.sidebar.write(
            f"📄 {file.name}"
        )


    process_button = st.sidebar.button(
        "🚀 Process Documents"
    )


    if process_button:

        all_documents = []


        with st.spinner(
            "Processing documents..."
        ):

            # ----------------------------------
            # Extract text from PDFs
            # ----------------------------------

            for uploaded_file in uploaded_files:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_path = temp_file.name


                try:

                    documents = extract_text_from_pdf(
                        temp_path
                    )


                    for document in documents:

                        document["source"] = (
                            uploaded_file.name
                        )


                    all_documents.extend(
                        documents
                    )


                finally:

                    if os.path.exists(
                        temp_path
                    ):

                        os.remove(
                            temp_path
                        )


            # ----------------------------------
            # Check documents
            # ----------------------------------

            if not all_documents:

                st.error(
                    "No readable text was found "
                    "in the uploaded PDFs."
                )


            else:

                # ----------------------------------
                # Create chunks
                # ----------------------------------

                chunks = create_chunks(
                    all_documents
                )


                # ----------------------------------
                # Create FAISS vector store
                # ----------------------------------

                vector_store = create_vector_store(
                    chunks
                )


                # ----------------------------------
                # Save in session state
                # ----------------------------------

                st.session_state.vector_store = (
                    vector_store
                )

                st.session_state.chunks = (
                    chunks
                )

                st.session_state.processed = (
                    True
                )

                st.session_state.chat_history = []


                st.success(
                    "Documents processed successfully! "
                    f"{len(chunks)} chunks created."
                )


# ==========================================
# CHAT SECTION
# ==========================================

st.subheader("💬 Ask Questions")


if st.session_state.processed:

    # ======================================
    # DISPLAY CHAT HISTORY
    # ======================================

    for question, answer, sources in (
        st.session_state.chat_history
    ):

        with st.chat_message("user"):

            st.write(question)


        with st.chat_message("assistant"):

            st.write(answer)


            if sources:

                st.write(
                    "### 📚 Sources"
                )


                displayed_sources = set()


                for source in sources:

                    source_key = (
                        source["source"],
                        source["page"]
                    )


                    if (
                        source_key
                        not in displayed_sources
                    ):

                        st.write(
                            f"📄 {source['source']} | "
                            f"Page {source['page']}"
                        )


                        displayed_sources.add(
                            source_key
                        )


    # ======================================
    # NEW QUESTION
    # ======================================

    question = st.chat_input(
        "Ask a question about your uploaded documents..."
    )


    if question:

        # ----------------------------------
        # User message
        # ----------------------------------

        with st.chat_message("user"):

            st.write(question)


        # ----------------------------------
        # Assistant message
        # ----------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching documents..."
            ):

                # ----------------------------------
                # Retrieve relevant documents
                # ----------------------------------

                retrieved_documents = (
                    search_vector_store(
                        st.session_state.vector_store,
                        st.session_state.chunks,
                        question,
                        k=3
                    )
                )


                # ----------------------------------
                # Generate answer
                # ----------------------------------

                answer = generate_answer(
                    question,
                    retrieved_documents
                )


                # ----------------------------------
                # Display answer
                # ----------------------------------

                st.write(answer)


                # ----------------------------------
                # Display sources
                # ----------------------------------

                if retrieved_documents:

                    st.write(
                        "### 📚 Sources"
                    )


                    displayed_sources = set()


                    for source in (
                        retrieved_documents
                    ):

                        source_key = (
                            source["source"],
                            source["page"]
                        )


                        if (
                            source_key
                            not in displayed_sources
                        ):

                            st.write(
                                f"📄 {source['source']} | "
                                f"Page {source['page']}"
                            )


                            displayed_sources.add(
                                source_key
                            )


                # ----------------------------------
                # Save chat history
                # ----------------------------------

                st.session_state.chat_history.append(
                    (
                        question,
                        answer,
                        retrieved_documents
                    )
                )


else:

    st.info(
        "👈 Upload one or more PDF documents "
        "from the sidebar and click "
        "**Process Documents** to start."
    )


# ==========================================
# CLEAR CHAT
# ==========================================

if st.sidebar.button(
    "🗑️ Clear Chat"
):

    st.session_state.chat_history = []

    st.rerun()