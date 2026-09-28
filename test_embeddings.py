from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

sentences = [
    "SQL for statistical data analysis",
    "Database querying and data management"
]

embeddings = model.encode(sentences)

print("Embedding shape:", embeddings.shape)
print("Embedding model working successfully!")