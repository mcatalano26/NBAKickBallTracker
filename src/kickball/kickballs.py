import sqlite3
from time import sleep

from nba_api.stats.endpoints import playbyplayv3  # type: ignore

from .db_updates import df_to_db
from .utils import get_git_root


def update_kickball_db() -> None:    
    conn = sqlite3.connect(f"{get_git_root()}/data/games.db")
    cursor = conn.cursor()
    cursor.execute("SELECT game_id FROM games")
    game_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    for game_id in game_ids:
        sleep(3)  # To avoid hitting API rate limits
        df = playbyplayv3.PlayByPlayV3(game_id).get_data_frames()[0]

        kick_df = df[df["description"].str.lower().str.contains("kick").reset_index(drop=True)]
        
        kick_df = kick_df[["gameId", "personId", "teamId", "description", "actionType", "subType", "videoAvailable", "actionId"]]
        
        df_to_db(kick_df, "kickballs", "append")