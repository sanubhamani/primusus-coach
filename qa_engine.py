import os
from pinecone import Pinecone as PineconeClient
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Set up embedding model
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Connect to Pinecone
pc = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("primusus-coach")

# Build vectorstore
vectorstore = Pinecone(index, embedding, "text")

# Set up GPT-4 model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Core response function
def get_response(user_input: str) -> str:
    # Retrieve top 3 matches
    results = vectorstore.similarity_search(user_input, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    prompt = f"""
You are the Primusus Coach.

Your tone is 80% Sage (insightful, clear, grounding) and 20% Commander (direct, no BS).

The user just asked: "{user_input}"

Based on the following course content:
{context}

Write a sharp, direct, human-sounding coaching reply. Keep it under 5 sentences.
""".strip()

    # Ask GPT-4
    response = llm.invoke(prompt)
    return response.content.strip()
