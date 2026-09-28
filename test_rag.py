from services.document_engine import (
    DocumentEngine
)

from services.ai_assistant import (
    AIAssistant
)


PDF_PATH = "uploads/sample.pdf"


# =====================================================
# LOAD DOCUMENT
# =====================================================

print(
    "Loading learning material..."
)

engine = DocumentEngine()


result = engine.process_pdf(
    PDF_PATH
)


print(
    f"Loaded {result['chunks']} chunks."
)


# =====================================================
# USER QUESTION
# =====================================================

question = input(
    "\nAsk Nexora something about the document: "
)


# =====================================================
# RETRIEVE RELEVANT INFORMATION
# =====================================================

retrieved_chunks = engine.search(
    question,
    top_k=3
)


print(
    "\nRetrieved relevant content."
)


# =====================================================
# GENERATE ANSWER
# =====================================================

assistant = AIAssistant()


answer = assistant.answer_question(
    question,
    retrieved_chunks
)


# =====================================================
# DISPLAY ANSWER
# =====================================================

print("\n")
print("=" * 60)
print("🤖 NEXORA AI LEARNING ASSISTANT")
print("=" * 60)

print(answer)


# =====================================================
# DISPLAY SOURCES
# =====================================================

print("\n")
print("=" * 60)
print("📚 RETRIEVED SOURCES")
print("=" * 60)


for i, chunk in enumerate(
    retrieved_chunks,
    start=1
):

    print(
        f"\nSource {i} "
        f"(similarity: {chunk['score']:.3f})"
    )