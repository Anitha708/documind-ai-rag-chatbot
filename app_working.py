import os
import tempfile
import streamlit as st

from document_loader import extract_text_from_pdf
from rag_pipeline import create_chunks, generate_answer
from vector_store import create_vector_store, search_vector_store


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM CSS ONLY
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #f7f8fc;
}

/* Main container */

.block-container {
    max-width: 1200px;
    padding-top: 35px;
    padding-bottom: 50px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Sidebar title */

.brand-title {
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 5px;
}

.brand-subtitle {
    color: #aeb7d0;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 30px;
}

/* Hero */

.hero-box {
    padding: 45px;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        #111827,
        #312e81,
        #4c1d95
    );
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 20px 60px rgba(49,46,129,0.22);
}

.hero-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #c7d2fe;
    margin-bottom: 15px;
}

.hero-heading {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1.5px;
}

.hero-text {
    max-width: 720px;
    margin-top: 18px;
    color: #dbe3f5;
    font-size: 16px;
    line-height: 1.7;
}

/* Cards */

.card {
    background: white;
    border: 1px solid #e6e8f0;
    border-radius: 20px;
    padding: 24px;
    min-height: 165px;
    box-shadow: 0 8px 30px rgba(15,23,42,0.05);
}

.card-icon {
    font-size: 25px;
    margin-bottom: 15px;
}

.card-title {
    font-size: 17px;
    font-weight: 700;
    color: #111827;
}

.card-text {
    color: #667085;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 8px;
}

/* Section title */

.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
    margin-top: 35px;
}

.section-text {
    color: #667085;
    font-size: 14px;
    margin-bottom: 15px;
}

/* Source */

.source-box {
    background: #f1f3ff;
    border: 1px solid #dfe3ff;
    padding: 12px 15px;
    border-radius: 12px;
    margin-top: 8px;
    font-size: 13px;
    color: #475467;
}

/* Status */

.status-box {
    padding: 13px;
    border-radius: 12px;
    background: rgba(255,255,255,0.07);
    margin-top: 15px;
    font-size: 13px;
    color: #cbd5e1;
}

/* Buttons */

.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}

/* Chat input */

[data-testid="stChatInput"] {
    border-radius: 16px;
}

/* Mobile */

@media(max-width: 768px) {

    .hero-box {
        padding: 30px;
    }

    .hero-heading {
        font-size: 36px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "🧠",
        help="DocuMind AI"
    )

    st.markdown(
        '<div class="brand-title">DocuMind AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="brand-subtitle">
        Intelligent document question answering powered
        by Retrieval-Augmented Generation.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📁 Knowledge Base")

    st.caption(
        "Upload PDF documents to create your private "
        "AI-powered knowledge base."
    )

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write("### Selected Documents")

        for file in uploaded_files:

            st.info(
                f"📄 {file.name}"
            )

        process = st.button(
            "🚀 Process Documents",
            use_container_width=True
        )

        if process:

            all_documents = []

            with st.spinner(
                "Processing your documents..."
            ):

                for uploaded_file in uploaded_files:

                    temp_path = None

                    try:

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".pdf"
                        ) as temp_file:

                            temp_file.write(
                                uploaded_file.getvalue()
                            )

                            temp_path = temp_file.name

                        documents = extract_text_from_pdf(
                            temp_path
                        )

                        for document in documents:
                            document["source"] = uploaded_file.name

                        all_documents.extend(documents)

                    finally:

                        if (
                            temp_path
                            and os.path.exists(temp_path)
                        ):
                            os.remove(temp_path)

                if not all_documents:

                    st.error(
                        "No readable text was found in the PDF."
                    )

                else:

                    chunks = create_chunks(
                        all_documents
                    )

                    vector_store = create_vector_store(
                        chunks
                    )

                    st.session_state.vector_store = vector_store
                    st.session_state.chunks = chunks
                    st.session_state.processed = True
                    st.session_state.chat_history = []

                    st.success(
                        f"Knowledge base ready • "
                        f"{len(chunks)} chunks"
                    )

    # Status

    if st.session_state.processed:

        st.markdown(
            f"""
            <div class="status-box">
            🟢 <b>AI system ready</b><br>
            {len(st.session_state.chunks)}
            document chunks indexed
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="status-box">
            🟡 <b>Waiting for documents</b><br>
            Upload a PDF to begin.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# PREMIUM HERO
# ============================================================

st.markdown(
    "✨ AI-POWERED DOCUMENT INTELLIGENCE"
)

st.title(
    "Ask your documents. Get intelligent answers."
)

st.write(
    "DocuMind AI uses Retrieval-Augmented Generation "
    "to understand your documents, retrieve relevant "
    "information, and provide grounded answers with "
    "document sources."
)

st.divider()


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 📄 Document Intelligence")

    st.caption(
        "Upload PDF documents and transform them "
        "into a searchable AI knowledge base."
    )


with col2:

    st.markdown("### 🔎 Smart Retrieval")

    st.caption(
        "Relevant document sections are retrieved "
        "before generating each answer."
    )


with col3:

    st.markdown("### 🤖 Grounded AI Answers")

    st.caption(
        "Answers are generated using your uploaded "
        "documents instead of invented information."
    )


# ============================================================
# CHAT TITLE
# ============================================================

st.markdown(
    """
    <div class="section-title">
    💬 Ask Questions
    </div>

    <div class="section-text">
    Ask anything related to your uploaded documents.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHAT HISTORY
# ============================================================

for question, answer, sources in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        st.write(answer)

        if sources:

            st.markdown("#### 📚 Sources")

            displayed_sources = set()

            for source in sources:

                source_key = (
                    source.get("source"),
                    source.get("page")
                )

                if source_key not in displayed_sources:

                    st.markdown(
                        f"""
                        <div class="source-box">
                        📄 <b>{source.get("source", "Unknown")}</b>
                        &nbsp; • &nbsp;
                        Page {source.get("page", "N/A")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    displayed_sources.add(
                        source_key
                    )


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        if not st.session_state.processed:

            st.warning(
                "Please upload and process a PDF first."
            )

        else:

            with st.spinner(
                "Searching your documents..."
            ):

                retrieved_documents = search_vector_store(
                    st.session_state.vector_store,
                    st.session_state.chunks,
                    question,
                    k=3
                )

            with st.spinner(
                "Generating answer..."
            ):

                answer = generate_answer(
                    question,
                    retrieved_documents
                )

            st.write(answer)

            if retrieved_documents:

                st.markdown("#### 📚 Sources")

                displayed_sources = set()

                for source in retrieved_documents:

                    source_key = (
                        source.get("source"),
                        source.get("page")
                    )

                    if source_key not in displayed_sources:

                        st.markdown(
                            f"""
                            <div class="source-box">
                            📄 <b>{source.get("source", "Unknown")}</b>
                            &nbsp; • &nbsp;
                            Page {source.get("page", "N/A")}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        displayed_sources.add(
                            source_key
                        )

            st.session_state.chat_history.append(
                (
                    question,
                    answer,
                    retrieved_documents
                )
            )