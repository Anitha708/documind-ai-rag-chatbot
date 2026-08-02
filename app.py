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
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM CSS
# IMPORTANT: ALL CSS IS INSIDE THIS STRING
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Inter, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(79,70,229,0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(14,165,233,0.12), transparent 28%),
        #080b14;
    color: #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* =========================================================
   BRAND
   ========================================================= */

.brand {
    text-align: center;
    padding: 25px 10px 35px 10px;
}

.brand-icon {
    font-size: 52px;
    margin-bottom: 8px;
}

.brand-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
}

.brand-subtitle {
    color: #94a3b8;
    font-size: 16px;
    margin-top: 8px;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid #20283a;
}

.sidebar-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* =========================================================
   BRIGHT PDF UPLOAD AREA
   ========================================================= */

[data-testid="stFileUploader"] {
    width: 100%;
}

[data-testid="stFileUploader"] section {
    background: linear-gradient(
        135deg,
        #17134f,
        #312e81
    ) !important;

    border: 2px dashed #818cf8 !important;
    border-radius: 18px !important;
    padding: 25px !important;
    min-height: 160px !important;

    box-shadow:
        0 0 20px rgba(99, 102, 241, 0.35),
        inset 0 0 20px rgba(99, 102, 241, 0.08) !important;
}

[data-testid="stFileUploader"] section:hover {
    background: linear-gradient(
        135deg,
        #1e1b65,
        #4338ca
    ) !important;

    border-color: #a5b4fc !important;

    box-shadow:
        0 0 30px rgba(99, 102, 241, 0.55) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] div {
    color: #ffffff !important;
}

[data-testid="stFileUploader"] button {
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    ) !important;

    color: #ffffff !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 12px 24px !important;

    box-shadow:
        0 5px 20px rgba(99, 102, 241, 0.55) !important;
}

[data-testid="stFileUploader"] button:hover {
    background: linear-gradient(
        135deg,
        #818cf8,
        #a78bfa
    ) !important;

    border-color: #ffffff !important;

    box-shadow:
        0 0 25px rgba(129, 140, 248, 0.75) !important;
}
/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #4f46e5;
    background: #4f46e5;
    color: white;
    font-weight: 700;
    min-height: 44px;
}

.stButton > button:hover {
    background: #6366f1;
    border-color: #818cf8;
}

/* =========================================================
   STATUS CARD
   ========================================================= */

.status-card {
    background: linear-gradient(
        135deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.95)
    );
    border: 1px solid #263247;
    border-radius: 16px;
    padding: 20px;
    margin-top: 15px;
}

.status-title {
    font-size: 12px;
    font-weight: 800;
    color: #94a3b8;
    letter-spacing: 1.5px;
}

.status-ready {
    color: #4ade80;
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
}

.status-waiting {
    color: #facc15;
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
}

.status-info {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 5px;
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 50px 20px;
    text-align: center;
}

.hero-label {
    color: #818cf8;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 15px;
}

.hero-title {
    font-size: 48px;
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: -2px;
}

.hero-description {
    max-width: 760px;
    margin: 20px auto 0 auto;
    color: #94a3b8;
    font-size: 17px;
    line-height: 1.7;
}

/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 30px;
}

.section-subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

/* =========================================================
   STAT CARDS
   ========================================================= */

.stat-card {
    background: #111827;
    border: 1px solid #263247;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    min-height: 145px;
}

.stat-icon {
    font-size: 30px;
}

.stat-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.stat-label {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 5px;
}

/* =========================================================
   FEATURE CARDS
   ========================================================= */

.feature-card {
    background: #111827;
    border: 1px solid #263247;
    border-radius: 16px;
    padding: 25px;
    min-height: 190px;
}

.feature-icon {
    font-size: 32px;
}

.feature-title {
    font-size: 18px;
    font-weight: 800;
    margin-top: 12px;
}

.feature-text {
    color: #94a3b8;
    line-height: 1.6;
    margin-top: 8px;
}

/* =========================================================
   CHAT
   ========================================================= */

.chat-box {
    background: #0f172a;
    border: 1px solid #263247;
    border-radius: 18px;
    padding: 25px;
    margin-top: 30px;
}

.chat-title {
    font-size: 25px;
    font-weight: 800;
}

.chat-subtitle {
    color: #94a3b8;
    margin-top: 5px;
}

/* =========================================================
   SOURCE CARD
   ========================================================= */

.source-card {
    background: #111827;
    border: 1px solid #263247;
    border-left: 4px solid #6366f1;
    border-radius: 10px;
    padding: 12px 15px;
    margin: 8px 0;
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# BRAND
# ============================================================

st.markdown("""
<div class="brand">
    <div class="brand-icon">🧠</div>
    <div class="brand-title">DocuMind AI</div>
    <div class="brand-subtitle">
        Intelligent document question answering powered by
        Retrieval-Augmented Generation.
    </div>
</div>
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

if "document_count" not in st.session_state:
    st.session_state.document_count = 0

if "page_count" not in st.session_state:
    st.session_state.page_count = 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📁 Knowledge Base</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload PDF documents to create your private "
        "AI-powered knowledge base."
    )

    st.markdown("### Upload PDF documents")

    # ========================================================
    # VISIBLE UPLOAD BUTTON
    # ========================================================

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF documents."
    )

    st.caption("Maximum 200MB per file • PDF only")

    # ========================================================
    # STATUS
    # ========================================================

    if st.session_state.processed:

        st.markdown("""
        <div class="status-card">
            <div class="status-title">SYSTEM STATUS</div>
            <div class="status-ready">
                🟢 DOCUMENTS READY
            </div>
            <div class="status-info">
                Your knowledge base is ready for questions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="status-card">
            <div class="status-title">SYSTEM STATUS</div>
            <div class="status-waiting">
                🟡 WAITING FOR DOCUMENTS
            </div>
            <div class="status-info">
                Upload a PDF to begin.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-label">✨ AI-POWERED DOCUMENT INTELLIGENCE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">'
    'Ask your documents.<br>'
    'Get intelligent answers.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-description">'
    'DocuMind AI uses Retrieval-Augmented Generation '
    'to understand your documents, retrieve relevant '
    'information, and provide grounded answers with '
    'document sources.'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# PROCESS DOCUMENTS
# ============================================================

if uploaded_files:

    st.markdown(
        '<div class="section-title">📚 Uploaded Documents</div>',
        unsafe_allow_html=True
    )

    for file in uploaded_files:
        st.write(f"📄 **{file.name}** — {file.size / 1024:.1f} KB")

    if st.button("🚀 Process Documents"):

        all_documents = []
        total_pages = 0

        progress = st.progress(0)

        with st.spinner("Processing your documents..."):

            for index, uploaded_file in enumerate(uploaded_files):

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

                    total_pages += len(documents)

                    for document in documents:

                        document["source"] = uploaded_file.name

                    all_documents.extend(documents)

                finally:

                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                progress.progress(
                    int(((index + 1) / len(uploaded_files)) * 100)
                )

        if not all_documents:

            st.error(
                "❌ No readable text was found in the uploaded PDF."
            )

        else:

            with st.spinner("Creating searchable knowledge base..."):

                chunks = create_chunks(all_documents)

                vector_store = create_vector_store(chunks)

            st.session_state.vector_store = vector_store
            st.session_state.chunks = chunks
            st.session_state.processed = True
            st.session_state.chat_history = []
            st.session_state.document_count = len(uploaded_files)
            st.session_state.page_count = total_pages

            st.success(
                f"✅ Documents processed successfully! "
                f"{len(chunks)} chunks created."
            )

            st.rerun()


# ============================================================
# KNOWLEDGE BASE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Knowledge Base Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Monitor your document intelligence workspace.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📄</div>
        <div class="stat-value">
            {st.session_state.document_count}
        </div>
        <div class="stat-label">DOCUMENTS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📑</div>
        <div class="stat-value">
            {st.session_state.page_count}
        </div>
        <div class="stat-label">PAGES</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🧩</div>
        <div class="stat-value">
            {len(st.session_state.chunks)}
        </div>
        <div class="stat-label">CHUNKS</div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    status = "Ready" if st.session_state.processed else "Waiting"
    icon = "🟢" if st.session_state.processed else "🟡"

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">{icon}</div>
        <div class="stat-value">
            {status}
        </div>
        <div class="stat-label">AI STATUS</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FEATURES
# ============================================================

st.markdown(
    '<div class="section-title">Built for intelligent document search</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'A retrieval-augmented workflow designed to provide '
    'answers grounded in your documents.'
    '</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">
            Document Intelligence
        </div>
        <div class="feature-text">
            Upload PDF documents and transform them
            into a searchable AI knowledge base.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔎</div>
        <div class="feature-title">
            Smart Retrieval
        </div>
        <div class="feature-text">
            Relevant document sections are retrieved
            before generating each answer.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">
            Grounded AI Answers
        </div>
        <div class="feature-text">
            Answers are generated using your uploaded
            documents instead of unrelated information.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHAT
# ============================================================

st.markdown("""
<div class="chat-box">
    <div class="chat-title">💬 Ask Questions</div>
    <div class="chat-subtitle">
        Ask anything related to your uploaded documents.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CHAT FUNCTIONALITY
# ============================================================

if st.session_state.processed:

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
                        source.get("source", "Unknown"),
                        source.get("page", "N/A")
                    )

                    if source_key not in displayed_sources:

                        st.markdown(
                            f"""
                            <div class="source-card">
                                📄 <b>{source_key[0]}</b>
                                &nbsp; | &nbsp;
                                Page {source_key[1]}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        displayed_sources.add(source_key)

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("🔎 Searching your documents..."):

                retrieved_documents = search_vector_store(
                    st.session_state.vector_store,
                    st.session_state.chunks,
                    question,
                    k=3
                )

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
                        source.get("source", "Unknown"),
                        source.get("page", "N/A")
                    )

                    if source_key not in displayed_sources:

                        st.markdown(
                            f"""
                            <div class="source-card">
                                📄 <b>{source_key[0]}</b>
                                &nbsp; | &nbsp;
                                Page {source_key[1]}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        displayed_sources.add(source_key)

            st.session_state.chat_history.append(
                (
                    question,
                    answer,
                    retrieved_documents
                )
            )

else:

    st.info(
        "👈 Upload a PDF from the sidebar to create your "
        "knowledge base and start asking questions."
    )


# ============================================================
# SIDEBAR CLEAR CHAT
# ============================================================

with st.sidebar:

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()