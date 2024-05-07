import os
import sys
import pandas as pd
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
from utils import load_split_df, chroma_upload_docs
from params import DATA_PATH
from typing import AnyStr

sub_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(sub_dir)

# Function for error handling and processing/uploading documents
def process_and_upload(chunk: pd.DataFrame or AnyStr, directory: AnyStr = DATA_PATH):
    """
    Use utils functions to process and upload the data to ChromaDB.

    Args:
        chunk (pd.DataFrame or String): The chunk of data to process and upload.
    """
    # Load and split the data
    if isinstance(chunk, pd.DataFrame):
        docs = load_split_df(chunk, data_type="dataframe")
    elif isinstance(chunk, str):
        docs = load_split_df(chunk, data_type="text")
    else:
        raise ValueError("Invalid data type. Must be a DataFrame or a String.")

    # Upload documents to ChromaDB
    chroma_upload_docs(docs, persist_directory=...)

if __name__ == "__main__":
    # Load the data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sub_dir = os.path.dirname(base_dir)
    rosters = pd.read_csv(os.path.join(sub_dir, 'nfl_data', 'rosters.csv'))
    rosters = rosters.loc[rosters['season'] > 2019, :] # test with a subset of the data
    stats = pd.read_csv(os.path.join(sub_dir, 'nfl_data', 'stats.csv'))
    stats = stats.loc[stats['season'] > 2019, :]
    wins = pd.read_csv(os.path.join(sub_dir, 'nfl_data', 'wins.csv'))
    wins = wins.loc[wins['season'] > 2019, :]


    # create semantic 'id' column for each DataFrame
    rosters['semantic_id'] = rosters['player_name'].astype(str) + ' in season number ' + rosters['season'].astype(str) + ' during week ' + rosters['week'].astype(str) + ' on the NFL team ' + rosters['team'].astype(str)
    stats['semantic_id'] = stats['player_name'].astype(str) + ' in season number ' + stats['season'].astype(str) + ' during week ' + stats['week'].astype(str) + ' on the NFL team ' + stats['recent_team'].astype(str) + ' with the position ' + stats['position'].astype(str)
    wins['semantic_id'] = wins['game_id'].astype(str) + ' in season number ' + wins['season'].astype(str) + ' in market type ' + wins['market_type'].astype(str) + ' in this sportsbook ' + wins['book'].astype(str)

    # Choose a chunking strategy (e.g., fixed size)
    chunksize = 100

    # Non-blocking execution and error handling with map_async
    pool = Pool(2)
    total_chunks = sum(len(df) // chunksize + 1 for df in [rosters, stats, wins])
    with tqdm(total=total_chunks) as pbar:
        for df in [rosters, stats, wins]:
            chunks = np.array_split(df, len(df) // chunksize + 1)
            for chunk in chunks:
                pool.apply_async(process_and_upload, args=(chunk,), callback=lambda _: pbar.update())

    # Close the pool and wait for all processes to complete
    pool.close()
    pool.join()
