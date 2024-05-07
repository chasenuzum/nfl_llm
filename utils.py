# script for loading csvs to dataframe and splitting into text
# work through splitter and embeddings

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.text_splitter import SemanticChunker

def embedding(model="llama2:7b"):
    """
    Load the embeddings
    """
    return OllamaEmbeddings(model=model)
    

def load_split_df(data, data_type = "dataframe"):
    """
        Load a miscellaneous data type and split into text
    """
    if data_type == "dataframe":
        docs = DataFrameLoader(data)
        docs.lazy_load()
        return docs
    elif data_type == "text":
        text_splitter = SemanticChunker(
               embedding(), breakpoint_threshold_type="standard_deviation")  
        docs = text_splitter.split_text(data)  
        return docs

def wiki_load(search_string : str, position = None, nfl_section = 'NFL Player'):
    """
    Load a wikipedia page for a player
    """
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    base_str = search_string + " " + nfl_section
    if position is not None:
        wiki_page = wikipedia.run(base_str + " " + position)
    else:
        wiki_page = wikipedia.run(base_str)
    return wiki_page

def chroma_upload_docs(docs : list, embedding_function = embedding(), persist_directory="./chroma_db"):
    """
    Bulk upload of files to a chromadb instance

    This script is designed to be used with the langchain_community package,
    and is a simple example of how to use the package to upload a large number of documents to a chromadb instance.
    """
    # create a vectorstore and save to disk
    return Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)