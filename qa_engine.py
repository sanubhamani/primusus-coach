import os
import openai
import pinecone
from langchain_community.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))

# Set up vector store
index_name = "primusus-coach"
embedding = OpenAIEmbeddings()
vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embedding)

# Main function
def get_response(user_input: str) -> str:
    # Search top 3 relevant chunks
    results = vectorstore.similarity_search(user_input, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    prompt = f"""
You are the Primusus Coach.

Your tone is 80% Sage (insightful, clear, grounding) and 20% Commander (direct, action-oriented). Keep it human, not robotic.

The user asked: "{user_input}"

Based on the following course content:
{context}

Write a 2–5 sentence reply that offers clarity, insight, and a specific suggestion the user can act on.
""".strip()

    # Call OpenAI
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return chat.choices[0].message["content"].strip()
