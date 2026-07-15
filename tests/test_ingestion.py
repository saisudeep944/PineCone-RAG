import os

from app.services.ingestion_service import (
    load_document,
    chunk_text
)

file_path = "data/AI_Medical_Device.pdf"

text = load_document(file_path)

file_name = os.path.basename(file_path)

source_type = file_name.split(".")[-1]

chunks = chunk_text(
    text=text,
    file_name=file_name,
    source_type=source_type
)

print("\nTOTAL CHUNKS:\n")
print(len(chunks))

print("\nFIRST CHUNK METADATA:\n")
print(chunks[0])