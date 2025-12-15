from typing import List, Optional
import pydantic


class RAGChunkAndSrc(pydantic.BaseModel):
    chunk: List[str]
    source_id: Optional[str] = None


class RAGUpsertResult(pydantic.BaseModel):
    ingested: int


class RAGSearchResult(pydantic.BaseModel):
    contexts: List[str] = []  # default empty list
    sources: List[str] = []   # default empty list


class RAGQueryResult(pydantic.BaseModel):
    answer: str
    sources: List[str] = []
    num_contexts: int
