# script for loading csvs to dataframe and splitting into text
# work through splitter and embeddings

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from chromadb import ChromaDB


def embed_text(text : str, model : str = 'en_core_web_lg'):
    """
    Embed text using spacy, or ollama if spacy is not available
    """
    try:
        return SpacyEmbeddings(model=model).embed_query(text)
    except:
        return OllamaEmbeddings(model=model).embed_query(text)

def load_split_embed(df : pd.DataFrame):
    """
    Load dataframe and split into text
    """
    loader = DataFrameLoader(df)
    loader.split_text()
    # create embeddings for each text


    return loader

def chroma_upload(embeddings : list, name : str, description : str = None, tags : list = None, private : bool = False):
    """
    embeddings : list of embeddings
    name : str, name of the document
    description : str, description of the document
    tags : list, tags for the document
    private : bool, whether the document is private
    """
    # create a new document
    doc = ChromaDB.per()
    doc.create_document(name=name, description=description, tags=tags, private=private)
    # upload embeddings
    doc.upload_embeddings(embeddings)
    # commit the document
    doc.commit_document()
    # return the document id
    return doc.document_id