import os
import sys
import pickle
from pathlib import Path
from base import SaveObjects
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

def load_data(raw_data_path : Path) -> list:
    loader=TextLoader(raw_data_path, encoding="utf-8")
    doc = loader.load()
    return doc

def chuncking(doc : list) -> list:
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    documents=text_splitter.split_documents(doc)
    return documents

def main():
    current_path = Path(__file__)
    root_path = current_path.parent.parent
    raw_data_path = root_path / sys.argv[1]
    processed_data_path = root_path / 'data' / 'processed' 
    processed_data_path.mkdir(exist_ok=True)
    doc = load_data(raw_data_path)
    documents = chuncking(doc)
    SaveObjects(path= processed_data_path / 'documents.pkl', object= documents)

if __name__ == "__main__":
    main()