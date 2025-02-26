from src.helper import load_pdf_file,text_split,download_hugging_face_embeddings
from pinecone import  Pinecone,ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"


def store_data_vector_db():
    extracted_data=load_pdf_file(data='data/')
    text_chunks=text_split(extracted_data)
    embeddings = download_hugging_face_embeddings()
    
    pc.create_index(
        name=index_name,
        dimension=384, 
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
    )

    PineconeVectorStore.from_documents(
        documents=text_chunks,
        index_name=index_name,
        embedding=embeddings, 
    )

if __name__ == '__main__':
    store_data_vector_db()