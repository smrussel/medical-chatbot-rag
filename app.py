from flask import Flask,render_template,jsonify,request
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

index_name = "medicalbot"

app = Flask(__name__)

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()


# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm = OpenAI(temperature=0.4, max_tokens=500)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route('/')
def chat_view():
    return render_template('index.html')


@app.route('/bot-response',methods=['GET','POST'])
def get_bot_response():
    data = request.get_json()
    print(data)
    msg= data.get('msg')
    response = rag_chain.invoke({'input':msg})
    print(response)
    print('Bot response',response['answer'])
    # return str(response['answer'])
    return jsonify({'bot_response':response['answer']})


if __name__ == '__main__':
    app.run(debug=True)