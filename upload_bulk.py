"""
Bulk upload of files to a chromadb instance

This script is designed to be used with the langchain_community package, 
and is a simple example of how to use the package to upload a large number of documents to a chromadb instance.

"""

import os
import sys
import pandas as pd
import numpy as np
from multiprocessing import Pool

# Add the base directory to the path
base_dir = os.path.dirname(os.path.abspath(__file__))
sub_dir = os.path.dirname(base_dir)
sys.path.insert(0, base_dir)

# load in constants                
from utils import load_split_df, chroma_upload_docs

# Function for error handling and processing/uploading documents
def process_and_upload(df_chunk):
    """
    Processes and uploads a DataFrame chunk to ChromaDB.

    Args:
        df_chunk (pd.DataFrame): The DataFrame chunk to process and upload.

    Raises:
        Exception: If any errors occur during processing or uploading.
    """

    try:
        docs = load_split_df(df_chunk, page_content_column='semantic_id')
        chroma_upload_docs(docs, persist_directory=sub_dir + '/nfl_data/ChromaDB')
    except Exception as e:
        print(f"Error processing and uploading chunk: {e}")
        # Consider adding more informative error logging or reporting here
        raise  # Re-raise the exception for handling in the main script

# Choose a chunking strategy (e.g., fixed size)
chunksize = 10000

if __name__ == "__main__":
    # Load the data
    rosters = pd.read_csv(sub_dir + '/nfl_data/rosters.csv')
    stats = pd.read_csv(sub_dir + '/nfl_data/stats.csv')
    wins = pd.read_csv(sub_dir + '/nfl_data/wins.csv')

    # create page content column or a sematic 'id' column
    rosters['semantic_id'] = rosters['player_name'].astype('str') + ' in season number ' + rosters['season'].astype('str') + ' during week ' + rosters['week'].astype('str') + ' on the NFL team ' + rosters['team'].astype('str')
    stats['semantic_id'] = stats['player_name'].astype('str') + ' in season number ' + stats['season'].astype('str') + ' during week ' + stats['week'].astype('str') + ' on the NFL team ' + stats['recent_team'].astype('str') + ' with the position ' + stats['position'].astype('str')
    wins['semantic_id'] = wins['game_id'].astype('str') + ' in season number ' + wins['season'].astype('str') + ' in market type ' + wins['market_type'].astype('str') + ' in this sportsbook ' + wins['book'].astype('str')

    # Load the data (assuming sub_dir and file paths are correct)
    rosters = pd.read_csv(sub_dir + '/nfl_data/rosters.csv')
    stats = pd.read_csv(sub_dir + '/nfl_data/stats.csv')
    wins = pd.read_csv(sub_dir + '/nfl_data/wins.csv')

    # Create page content columns (can optimize if needed)
    rosters['semantic_id'] = rosters['player_name'].astype('str') + ' in season number ' + rosters['season'].astype('str') + ' during week ' + rosters['week'].astype('str') + ' on the NFL team ' + rosters['team'].astype('str')
    stats['semantic_id'] = stats['player_name'].astype('str') + ' in season number ' + stats['season'].astype('str') + ' during week ' + stats['week'].astype('str') + ' on the NFL team ' + stats['recent_team'].astype('str') + ' with the position ' + stats['position'].astype('str')
    wins['semantic_id'] = wins['game_id'].astype('str') + ' in season number ' + wins['season'].astype('str') + ' in market type ' + wins['market_type'].astype('str') + ' in this sportsbook ' + wins['book'].astype('str')


    # Non-blocking execution and error handling with map_async
    pool = Pool(os.cpu_count()-2)
    map_async_results = pool.map_async(process_and_upload, (chunk for df in [rosters, stats, wins] for chunk in np.array_split(df, len(df) // chunksize + 1)))

    # Collect results and close the pool
    map_async_results.wait()
    pool.close()
    pool.join()