from app.services.ingestion_service import (
    ingest_document
)


file_path= "data/AI_Medical_Device.pdf"

result = ingest_document(
    file_path=file_path,
    namespace="AI_Medical_Device"
)

print(result)