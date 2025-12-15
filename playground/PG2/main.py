import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime
from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage
from custom_types import RAGChunkAndSrc, RAGQueryResult, RAGSearchResult, RAGUpsertResult

load_dotenv()

inngest_client = inngest.Inngest(
    app_id="Nerdial",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer(),
)


@inngest_client.create_function(
    fn_id= "my_function",
    trigger= inngest.TriggerEvent(event="Nerdial/my_function")
)
async def my_function(
    ctx: inngest.Context,
):
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc:
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.get("source_id", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path)
        return RAGChunkAndSrc(chunk=chunks, source_id=source_id)

    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult:
        chunks = chunks_and_src.chunk
        source_id = chunks_and_src.source_id
        vecs = embed_texts(chunks)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, name=f"{source_id}-{i}")) for i in range(len(vecs))]
        payloads = [{"source": source_id, "text": chunks[i]} for i in range(len(chunks))]
        QdrantStorage().upsert(ids, vecs, payloads)
        return RAGUpsertResult(inngested=len(chunks))

    chuck_and_src = await ctx.step.run(
        lambda: _load(ctx),
        step_id="load_and_chunk",
        output_type=RAGChunkAndSrc,
    )
    
    inngested = await ctx.step.run(
        lambda: _upsert(chuck_and_src),
        step_id="embed_and_upsert",
        output_type=RAGUpsertResult,
    )


    return inngested.model_dump()

#    return {"Hello":"World!"}

@inngest_client.create_function(
    fn_id="RAG: Query PDF",
    trigger=inngest.TriggerEvent(event="rag/query_pdf_ai"),
    throttle=inngest.Throttle(
        limit=2,
        period=datetime.timedelta(minutes=1)
    ),
    rate_limit=inngest.RateLimit(
        limit=1,
        period=datetime.timedelta(hours=4),
        key="event.data.source_id"
    )
)


async def rag_query_pdf_ai(ctx: inngest.Context) -> RAGSearchResult:
    def _search(question: str, top_k: int=5):
        query_vec = embed_texts([question])[0]
        store = QdrantStorage()
        found = store.search(query_vec, top_k=top_k)
        return RAGSearchResult(contexts=found["contexts"], sources=found["sources"])


    question = ctx.event.data["question"]
    top_k = ctx.event.data.get("top_k", 5)

    found = await ctx.step.run(
    lambda: _search(question, top_k=top_k),
    step_id="embed_and_search",
    output_type=RAGSearchResult
    )

    context_block= "\n\n".join(f"- {c}"for c in found.contexts)
    user_content = (
        "Use the following context to answer the question:\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question:{question}\n\n"
        "Answer concisely using the context above."
    ) 

    adapter = ai.openai.Adapter(
        auth_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
    )

    res = await ctx.step.ai.infer(
        "llm-answer", 
        adapter=adapter,
        body={
            "max_tokens": 1024,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_content}   
            ]
        }
    )

    answer = res["choices"][0]["message"]["content"].strip()
    return {"answer": answer, "source": found.sources, "num_contexts": len(found.contexts)}

app = FastAPI()

inngest.fast_api.serve(app, inngest_client, functions=[my_function, rag_query_pdf_ai])
