# script for loading csvs to dataframe and splitting into text
# work through splitter and embeddings

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def embedding(model="llama2"):
    """
    Load the embeddings
    """
    return OllamaEmbeddings(model=model)
    

def load_split_df(df : pd.DataFrame, **kwargs):
    """
    Load dataframe and split into text
    """
    docs = DataFrameLoader(df, **kwargs).load()
    return docs

def chroma_upload_docs(docs : list, embedding_function = embedding(), persist_directory="./chroma_db"):
    """
    Bulk upload of files to a chromadb instance

    This script is designed to be used with the langchain_community package,
    and is a simple example of how to use the package to upload a large number of documents to a chromadb instance.
    """
    # create a vectorstore and save to diskß
    return Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)