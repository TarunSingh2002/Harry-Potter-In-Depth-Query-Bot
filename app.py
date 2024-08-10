import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, render_template, request, jsonify
from langchain.chains.combine_documents import create_stuff_documents_chain
import threading

app = Flask(__name__)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Global variable for retrieval_chain
retrieval_chain = None
lock = threading.Lock()  # Add a lock for thread-safe access to shared resources

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

def main():
    global retrieval_chain
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
    if request.method == 'POST':
        user_input = request.json.get('input_text')
        
        with lock: 
            response = retrieval_chain.invoke({"input": user_input})
        
        answer = response['answer']
        return jsonify({'answer': answer})

    return render_template('index.html')

if __name__ == "__main__":
    main()
    app.run(debug=True, threaded=True) 