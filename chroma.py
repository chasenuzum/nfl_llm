import chromadb
import os

sub_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(sub_dir)
# Example setup of the client to connect to your chroma server
client = chromadb.HttpClient(host='localhost', port=8000)