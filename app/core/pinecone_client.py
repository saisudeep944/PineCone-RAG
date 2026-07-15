from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")

pc = Pinecone(api_key=api_key)

index = pc.Index(index_name)

print("Connected to Pinecone successfully")