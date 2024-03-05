import os
import sys
import pandas as pd
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
from utils import load_split_df, chroma_upload_docs
from params import DATA_PATH

sub_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(sub_dir)

# Function for error handling and processing/uploading documents
def process_and_upload(chunk):
    """
    Processes and uploads a DataFrame chunk to ChromaDB.

    Args:
        chunk (pd.DataFrame): The DataFrame chunk to process and upload.
    """
    try:
        # Load and split DataFrame chunk
        docs = load_split_df(chunk, page_content_column='semantic_id')
        # Upload documents to ChromaDB
        chroma_upload_docs(docs, persist_directory=sub_dir + '/' +DATA_PATH)
    except Exception as e:
        print(f"Error processing and uploading chunk: {e}")

if __name__ == "__main__":
    # Load the data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sub_dir = os.path.dirname(base_dir)
    rosters = pd.read_csv(os.path.join(sub_dir, 'nfl_data', 'rosters.csv'))
    stats = pd.read_csv(os.path.join(sub_dir, 'nfl_data', 'stats.csv'))
    wins = pd.read_csv(os.path.join(sub_dir, 'nfl_data', 'wins.csv'))

    # create semantic 'id' column for each DataFrame
    rosters['semantic_id'] = rosters['player_name'].astype(str) + ' in season number ' + rosters['season'].astype(str) + ' during week ' + rosters['week'].astype(str) + ' on the NFL team ' + rosters['team'].astype(str)
    stats['semantic_id'] = stats['player_name'].astype(str) + ' in season number ' + stats['season'].astype(str) + ' during week ' + stats['week'].astype(str) + ' on the NFL team ' + stats['recent_team'].astype(str) + ' with the position ' + stats['position'].astype(str)
    wins['semantic_id'] = wins['game_id'].astype(str) + ' in season number ' + wins['season'].astype(str) + ' in market type ' + wins['market_type'].astype(str) + ' in this sportsbook ' + wins['book'].astype(str)

    # Choose a chunking strategy (e.g., fixed size)
    chunksize = 1000

    # Non-blocking execution and error handling with map_async
    pool = Pool(os.cpu_count() - 2)
    total_chunks = sum(len(df) // chunksize + 1 for df in [rosters, stats, wins])
    with tqdm(total=total_chunks) as pbar:
        for df in [rosters, stats, wins]:
            chunks = np.array_split(df, len(df) // chunksize + 1)
            for chunk in chunks:
                pool.apply_async(process_and_upload, args=(chunk,), callback=lambda _: pbar.update())

    # Close the pool and wait for all processes to complete
    pool.close()
    pool.join()
