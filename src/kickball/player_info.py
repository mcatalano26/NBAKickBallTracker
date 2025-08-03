import sqlite3
from datetime import date
from time import sleep

import pandas as pd  # type: ignore
from nba_api.stats.endpoints import boxscoreplayertrackv3  # type: ignore

from .db_updates import df_to_db
from .utils import display_progress_bar, get_games_for_date_range, get_git_root


def update_minutes_db(start_date: date, end_date: date) -> None:
    game_ids = get_games_for_date_range(start_date, end_date)
    
    conn = sqlite3.connect(f"{get_git_root()}/data/minutes.db")
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS minutes (
                       gameId TEXT,
                       personId INTEGER,
                       minutes TEXT,
                       UNIQUE(gameId, personId)
                   )
                ''')
    cursor.execute('''
                   CREATE UNIQUE INDEX IF NOT EXISTS idx_gameId_personId ON minutes(gameId, personId) 
                ''')
    conn.close()
    
    total_games = len(game_ids)
    minutes_df = pd.DataFrame()
    for idx, game_id in enumerate(game_ids, 1):
        sleep(1)  # To avoid hitting API rate limits
        df = boxscoreplayertrackv3.BoxScorePlayerTrackV3(game_id)
        
        game_df = df.player_stats.get_data_frame()
        game_df = game_df[["gameId", "personId", "minutes"]]
        
        minutes_df = pd.concat([minutes_df, game_df], ignore_index=True)
        
        display_progress_bar(idx, total_games, "Minutes Data Fetch")
        
    print("Minutes data fetched successfully. Updating database...")
    df_to_db(minutes_df, "minutes", "append")
    print(f"Minutes database updated for games from {start_date} to {end_date}.")