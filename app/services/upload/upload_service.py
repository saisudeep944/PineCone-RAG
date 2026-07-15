import os

import uuid

from pathlib import Path

from app.services.ingestion_service import (
    ingest_document
)


UPLOAD_DIR = "uploaded_docs"

os.makedirs(

    UPLOAD_DIR,

    exist_ok=True
)


def process_uploaded_file(

    uploaded_file
):

    unique_namespace = (

        Path(
            uploaded_file.filename
        ).stem

        +

        "_"

        +

        str(uuid.uuid4())[:8]
    )

    file_path = os.path.join(

        UPLOAD_DIR,

        uploaded_file.filename
    )

    with open(

        file_path,

        "wb"
    ) as f:

        f.write(

            uploaded_file.file.read()
        )

    ingest_document(

    file_path=file_path,

    namespace=unique_namespace
        )

    return {

        "namespace":
        unique_namespace,

        "file_name":
        uploaded_file.filename
    }