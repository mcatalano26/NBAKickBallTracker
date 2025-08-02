import sqlite3
from datetime import date
from time import sleep

import pandas as pd  # type: ignore
from nba_api.stats.endpoints import playbyplayv3  # type: ignore

from .db_updates import df_to_db
from .utils import get_git_root


def update_kickball_db(start_date: date, end_date: date) -> None:    
    conn = sqlite3.connect(f"{get_git_root()}/data/games.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT game_id FROM games WHERE game_date >= ? AND game_date <= ?",
        (start_date.isoformat(), end_date.isoformat())
    )
    game_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    conn = sqlite3.connect(f"{get_git_root()}/data/kickballs.db")
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS kickballs (
                       gameId TEXT,
                       personId INTEGER,
                       teamID INTEGER,
                       description TEXT,
                       actionType TEXT,
                       subType TEXT,
                       videoAvailable INTEGER,
                       actionId INTEGER,
                       UNIQUE(gameId, actionId)
                    )
                ''')
    cursor.execute('''
                     CREATE UNIQUE INDEX IF NOT EXISTS idx_gameId_actionId ON kickballs(gameId, actionId)                  
                ''')
    conn.close()

    total_games = len(game_ids)
    kick_df = pd.DataFrame()
    for idx, game_id in enumerate(game_ids, 1):
        sleep(3)  # To avoid hitting API rate limits
        df = playbyplayv3.PlayByPlayV3(game_id).get_data_frames()[0]
        
        game_df = df[df["description"].str.lower().str.contains("kick").reset_index(drop=True)]
        
        game_df = game_df[["gameId", "personId", "teamId", "description", "actionType", "subType", "videoAvailable", "actionId"]]
        
        kick_df = pd.concat([kick_df, game_df], ignore_index=True)

        percent = int((idx / total_games) * 100)
        bar = ('#' * (percent // 2)).ljust(50)
        print(f"\rProgress: |{bar}| {percent}% ({idx}/{total_games})", end='', flush=True)
    print()  # Move to next line after progress bar
    
    print("Kickball data fetched successfully. Updating database...")
    df_to_db(kick_df, "kickballs", "append")
        
    print(f"Kickball database updated for games from {start_date} to {end_date}.")