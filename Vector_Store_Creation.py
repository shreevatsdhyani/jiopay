import pickle
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from groq import Groq

# Load processed documents
with open("processed_docs.pkl", "rb") as f:
    documents = pickle.load(f)

print(f"Loaded {len(documents)} document chunks.")

# Ensure embeddings are loaded correctly
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vector store
vector_store = FAISS.from_texts(
    texts=[doc["text"] for doc in documents],
    embedding=embeddings,
    metadatas=[doc["metadata"] for doc in documents]
)

# Save FAISS index locally
vector_store.save_local("jiopay_index")
print("FAISS Vector Store saved successfully.")

# Querying Using Groq API
groq_api_key = "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"  # Replace with your actual API key
client = Groq(api_key=groq_api_key)

query = "How do I recharge using JioPay?"
retrieved_docs = vector_store.similarity_search(query, k=3)

# Prepare input for Groq API
retrieved_texts = "\n\n".join([doc.page_content for doc in retrieved_docs])

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": "You are a helpful JioPay assistant. Answer only using the provided data."},
        {"role": "user", "content": f"Based on this data, provide a step-by-step guide for recharging using JioPay:\n\n{retrieved_texts}"}
    ]
)

print("Groq AI Response:", response.choices[0].message.content)
