from pydantic import BaseModel
from typing import List

class CreateSessionRequest(
    BaseModel
):

    namespace: str


class CreateSessionResponse(
    BaseModel
):

    session_id: str

    namespace: str


class ChatRequest(
    BaseModel
):

    session_id: str

    message: str



class SourceResponse(
    BaseModel
):

    file_name: str

    chunk_index: int

    rerank_score: float

    text: str    


class ChatResponse(
    BaseModel
):

    status: str

    intent: str

    answer: str

    sources: List[
        SourceResponse
    ]
class SwitchNamespaceRequest(
    BaseModel
):

    session_id: str

    namespace: str