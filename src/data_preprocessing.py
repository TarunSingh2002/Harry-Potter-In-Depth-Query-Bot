import os
import sys
import pickle
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

from langchain_community.vectorstores.chroma import Chroma

def making_vector_db(documents: list, persist_directory: Path) -> Chroma:
    db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=str(persist_directory))
    return db

def main():
    current_path = Path(__file__)
    root_path = current_path.parent.parent

    processed_data_path = root_path / sys.argv[1]

    vector_db_data_path = root_path / 'data' / 'vector_db'
    vector_db_data_path.mkdir(exist_ok=True)

    with open(processed_data_path, 'rb') as file:
        documents = pickle.load(file)

    db = making_vector_db(documents, vector_db_data_path)

    print("Vector store has been successfully created and persisted at:", vector_db_data_path)

if __name__ == "__main__":
    main()
