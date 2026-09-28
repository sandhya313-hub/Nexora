from services.document_engine import (
    DocumentEngine
)


PDF_PATH = "uploads/sample.pdf"


engine = DocumentEngine()


result = engine.process_pdf(
    PDF_PATH
)


print("\n==============================")
print("DOCUMENT PROCESSING")
print("==============================")

print(
    "Characters:",
    result["characters"]
)

print(
    "Chunks:",
    result["chunks"]
)


query = input(
    "\nAsk something about the document: "
)


results = engine.search(
    query,
    top_k=3
)


print("\n==============================")
print("RELEVANT CONTENT")
print("==============================")


for i, result in enumerate(
    results,
    start=1
):

    print(
        f"\n--- Result {i} "
        f"(score: {result['score']:.3f}) ---\n"
    )

    print(
        result["text"][:1000]
    )