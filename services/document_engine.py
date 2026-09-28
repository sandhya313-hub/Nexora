from pathlib import Path

from pypdf import PdfReader

from sentence_transformers import SentenceTransformer

import faiss
import numpy as np


class DocumentEngine:

    def __init__(self):

        print("Loading document embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.chunks = []

        self.index = None

        print("Document engine ready!")


    # =====================================================
    # PDF TEXT EXTRACTION
    # =====================================================

    def extract_text(self, pdf_path):

        reader = PdfReader(
            pdf_path
        )

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pages.append(text)


        return "\n".join(pages)


    # =====================================================
    # TEXT CHUNKING
    # =====================================================

    def create_chunks(
        self,
        text,
        chunk_size=800,
        overlap=150
    ):

        words = text.split()

        chunks = []

        start = 0


        while start < len(words):

            end = start + chunk_size

            chunk = " ".join(
                words[start:end]
            )

            if chunk.strip():

                chunks.append(
                    chunk
                )

            start += (
                chunk_size - overlap
            )


        return chunks


    # =====================================================
    # BUILD VECTOR INDEX
    # =====================================================

    def build_index(
        self,
        chunks
    ):

        self.chunks = chunks


        embeddings = self.model.encode(
            chunks,
            normalize_embeddings=True
        )


        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )


        dimension = embeddings.shape[1]


        self.index = faiss.IndexFlatIP(
            dimension
        )


        self.index.add(
            embeddings
        )


        return len(chunks)


    # =====================================================
    # PROCESS PDF
    # =====================================================

    def process_pdf(
        self,
        pdf_path
    ):

        text = self.extract_text(
            pdf_path
        )


        if not text.strip():

            raise ValueError(
                "No readable text found in PDF."
            )


        chunks = self.create_chunks(
            text
        )


        self.build_index(
            chunks
        )


        return {
            "characters": len(text),
            "chunks": len(chunks)
        }


    # =====================================================
    # SEMANTIC SEARCH
    # =====================================================

    def search(
        self,
        query,
        top_k=3
    ):

        if self.index is None:

            return []


        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )


        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )


        scores, indices = self.index.search(
            query_embedding,
            min(
                top_k,
                len(self.chunks)
            )
        )


        results = []


        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue


            results.append({
                "text": self.chunks[index],
                "score": float(score)
            })


        return results