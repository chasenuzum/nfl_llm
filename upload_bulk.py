"""
Bulk upload of files to a chromadb instance

This script is designed to be used with the langchain_community package, 
and is a simple example of how to use the package to upload a large number of documents to a chromadb instance.

"""

import os
import sys
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
sub_dir = os.path.dirname(base_dir)
print(base_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# load in constants                
from utils import load_split_df, chroma_upload_docs
from params import CHROMADB_PATH

# Load the data
rosters = pd.read_csv(sub_dir + '/nfl_data/rosters.csv')
stats = pd.read_csv(sub_dir + '/nfl_data/stats.csv')
wins = pd.read_csv(sub_dir + '/nfl_data/wins.csv')

# create page content column or a sematic 'id' column
rosters['semantic_id'] = rosters['player_name'].astype('str') + ' in season number ' + rosters['season'].astype('str') + ' during week ' + rosters['week'].astype('str') + ' on the NFL team ' + rosters['team'].astype('str')
stats['semantic_id'] = stats['player_name'].astype('str') + ' in season number ' + stats['season'].astype('str') + ' during week ' + stats['week'].astype('str') + ' on the NFL team ' + stats['recent_team'].astype('str') + ' with the position ' + stats['position'].astype('str')
wins['semantic_id'] = wins['game_id'].astype('str') + ' in season number ' + wins['season'].astype('str') + ' in market type ' + wins['market_type'].astype('str') + ' in this sportsbook ' + wins['book'].astype('str')


# Split the data into text and upload to chromadb
for i in [rosters, stats, wins]:
    docs = load_split_df(i, page_content_column='semantic_id')
    chroma_upload_docs(docs, persist_directory=CHROMADB_PATH)