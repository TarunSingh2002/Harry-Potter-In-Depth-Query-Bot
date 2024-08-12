import os
import awsgi
import threading
from pathlib import Path
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, render_template, request, jsonify
from langchain.chains.combine_documents import create_stuff_documents_chain

app = Flask(__name__)
CORS(app)

openai_api_key = os.environ["OPENAI_API_KEY"]
langchain_api_key = os.environ["LANGCHAIN_API_KEY"]
langchain_project = os.environ["LANGCHAIN_PROJECT"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"

retrieval_chain = None
lock = threading.Lock()

def load_vector_db(persist_directory: Path) -> Chroma:
    db = Chroma(persist_directory=str(persist_directory), embedding_function=OpenAIEmbeddings())
    return db

def create_prompt():
    prompt = ChatPromptTemplate.from_template("""
    Answer the following questions based only on the provided context.
    Think step by step before providing a detailed answer.
    <context>
    {context}
    </context>
    Question: {input}
    """)
    return prompt

def initialize_retrieval_chain():
    global retrieval_chain
    if retrieval_chain is None:
        current_path = Path(__file__)
        root_path = current_path.parent
        vector_db_data_path = root_path / 'data' / 'vector_db'

        llm = ChatOpenAI(model="gpt-3.5-turbo")

        prompt = create_prompt()
        db = load_vector_db(persist_directory=vector_db_data_path)
        retriever = db.as_retriever()

        document_chain = create_stuff_documents_chain(llm, prompt)

        retrieval_chain = create_retrieval_chain(retriever, document_chain)

@app.route('/', methods=['GET', 'POST'])
def index():
    initialize_retrieval_chain()
    
    if request.method == 'POST':
        user_input = request.json.get('input_text')

        with lock:
            response = retrieval_chain.invoke({"input": user_input})
        
        answer = response['answer']
        return jsonify({'answer': answer})

    return render_template('index.html')

if __name__ == "__main__":
    initialize_retrieval_chain()
    app.run(debug=True, threaded=True)

def handler(event, context):
    initialize_retrieval_chain()
    event['queryStringParameters'] = event.get('queryStringParameters', {})
    return awsgi.response(app, event, context)