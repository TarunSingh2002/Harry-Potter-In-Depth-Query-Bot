import os
import threading
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from werkzeug.middleware.proxy_fix import ProxyFix
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from aws_lambda_wsgi import response as wsgi_response
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, render_template, request, jsonify
from langchain.chains.combine_documents import create_stuff_documents_chain

app = Flask(__name__)

# API keys and project name are now read directly from environment variables
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

        # Debugging logs
        print("Initializing retrieval chain...")
        print(f"Vector DB Path: {vector_db_data_path}")
        print(f"LangChain Project: {langchain_project}")

        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key, project_name=langchain_project)

        prompt = create_prompt()
        db = load_vector_db(persist_directory=vector_db_data_path)
        retriever = db.as_retriever()

        document_chain = create_stuff_documents_chain(llm, prompt)

        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        print("Retrieval chain initialized successfully.")

@app.route('/', methods=['GET', 'POST'])
def index():
    initialize_retrieval_chain()
    if request.method == 'POST':
        # Debugging log to check if request received
        print("POST request received.")
        try:
            user_input = request.json.get('input_text')
            print(f"User Input: {user_input}")  # Log input

            with lock:
                response = retrieval_chain.invoke({"input": user_input})

            answer = response['answer']
            print(f"Generated Answer: {answer}")  # Log output

            return jsonify({'answer': answer})

        except Exception as e:
            # Log any exception that occurs
            print(f"Error during request processing: {e}")
            return jsonify({'error': str(e)}), 500

    # Debugging log to check if GET request is working
    print("GET request received.")
    return render_template('index.html')

# if __name__ == "__main__":
#     initialize_retrieval_chain()
#     app.run(debug=True, threaded=True)

def handler(event, context):
    initialize_retrieval_chain()
    return wsgi_response(app, event, context)