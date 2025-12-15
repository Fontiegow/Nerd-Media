import os
from openai import OpenAI
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv

load_dotenv()  # load .env before creating client

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment!")

client = OpenAI(api_key=api_key)  # pass it explicitly

EMBEDDING_MODEL = "text-embedding-3-small"
EMBED_DIM = 3072

splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)

def load_and_chunk_pdf(file_path: str):
    docs = PDFReader().load_data(file_path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL,
        dimensions=EMBED_DIM,
    )
    return [r.embedding for r in response.data]
