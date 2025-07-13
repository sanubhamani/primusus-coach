import os
from openai import OpenAI
import openai
from pinecone import Pinecone as PineconeClient
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define OpenAI embedding model with explicit client to avoid proxies error
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    client=OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.openai.com/v1"
    )
)

# Connect to Pinecone index
pc = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("primusus-coach")

# Build vector store using LangChain wrapper
vectorstore = Pinecone(index, embedding, "text")  # "text" is the metadata key

# Core response function
def get_response(user_input: str) -> str:
    # Retrieve top 3 relevant chunks from Pinecone
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

    # Call GPT-4 with composed prompt
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return chat.choices[0].message["content"].strip()
