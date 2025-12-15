from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model  = OllamaLLM(model="llama3.2")

template= """
You are an expert in answering questions about a pizza restaurant.

Here is some relaven review of the restaurant:
{review}

Answer the following question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True: 
    question = input("Ask a question (q for quit): ")
    if question == "q":
        break

    reviews = retriever.invoke(question)
    result = chain.invoke({
        "review": reviews,
        "question": question
    })
    print(result)
