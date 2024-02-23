# script for exploring nfl-stats dataframes

import pandas as pd
import nfl_data_py as nfl
import os

# set file to base directory based on current file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
# create directory for nfl data
os.makedirs(base_dir + '/nfl_data', exist_ok=True)
database_path = base_dir + '/nfl_data/nfl.db'  # Replace with your actual path

def download_data(years : list):
    """
    Download data from nfl_data_py and save to csv
    do so in yearly chunks as to not overrun the server
    and in list comprehension to avoid for loops
    and upload to a sqlite database

    Args:
        years (list): list of years to download

    Returns:
        None
    """
    # import total wins and upload to csv and sqlite
    wins = pd.concat([nfl.import_win_totals(years=[i]) for i in years])
    # csv
    wins.to_csv(base_dir + '/nfl_data/wins.csv')
    # sqlite
    wins.to_sql('wins', database_path, if_exists='replace')

    # import weekly rosters
    rosters = pd.concat([nfl.import_weekly_rosters(years=[i]) for i in years])
    rosters.to_csv(base_dir + '/nfl_data/rosters.csv')
    rosters.to_sql('rosters', database_path, if_exists='replace')

    # import weekly stats
    stats = pd.concat([nfl.import_weekly_data(years=[i]) for i in years])
    stats.to_csv(base_dir + '/nfl_data/stats.csv')
    stats.to_sql('stats', database_path, if_exists='replace')

years = list(range(2008, 2023))
download_data(years)