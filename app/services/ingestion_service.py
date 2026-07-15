import os

from app.services.loaders.pdf_loader import load_pdf
from app.services.loaders.txt_loader import load_txt
from app.services.loaders.docx_loader import load_docx
from app.services.loaders.csv_loader import load_csv
import uuid
from datetime import datetime
from app.services.embedding_service import (generate_embeddings)
from app.services.pinecone_service import (bulk_upsert)

def load_document(file_path: str):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".txt":
        return load_txt(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    elif extension == ".csv":
        return load_csv(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )





def chunk_text(
    text: str,
    file_name: str,
    source_type: str,
    chunk_size: int = 500,
    overlap: int = 50
):

    chunks = []

    document_id = str(uuid.uuid4())

    start = 0
    chunk_index = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end]

        chunk_data = {
            "document_id": document_id,
            "chunk_id": f"{document_id}_{chunk_index}",
            "chunk_index": chunk_index,
            "text": chunk_text,
            "file_name": file_name,
            "source_type": source_type,
            "upload_time": str(datetime.utcnow())
        }

        chunks.append(chunk_data)

        chunk_index += 1

        start += chunk_size - overlap

    return chunks




def ingest_document(file_path: str,namespace: str
):

    text = load_document(file_path)

    file_name = os.path.basename(file_path)

    source_type = file_name.split(".")[-1]

    chunks = chunk_text(
        text=text,
        file_name=file_name,
        source_type=source_type
    )

    chunk_texts = [
        chunk["text"] for chunk in chunks
    ]

    embeddings = generate_embeddings(chunk_texts)

    total_vectors = bulk_upsert(
    chunks,
    embeddings,
    namespace
    )

    return {
        "file_name": file_name,
        "total_chunks": len(chunks),
        "vectors_stored": total_vectors
    }