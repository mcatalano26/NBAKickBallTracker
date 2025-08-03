import sqlite3
from dataclasses import dataclass
from datetime import date

import pandas as pd  # type: ignore

from .utils import get_games_for_date_range, get_git_root


@dataclass
class Podium:
    Gold: str
    Silver: str
    Bronze: str
 

def get_df(db_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(f"{get_git_root()}/data/{db_name}.db")
    sql_query = f"SELECT * FROM {db_name}"
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

def get_game_range_df(game_ids: list[str], db_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(f"{get_git_root()}/data/{db_name}.db")
    sql_query = f"SELECT * FROM {db_name} WHERE gameId IN ({{}})".format(','.join('?' for _ in game_ids))
    df = pd.read_sql(sql_query, conn, params=game_ids)
    conn.close()
    return df

def get_podium(start_date: date, end_date: date) -> Podium:
    game_ids = get_games_for_date_range(start_date, end_date)
    
    minutes_df = get_game_range_df(game_ids, "minutes")
    kick_df = get_game_range_df(game_ids, "kickballs")
    players_df = get_df("players")
    
    print(minutes_df)
    print(kick_df)
    print(players_df)
    
    return Podium(Gold="Player A", Silver="Player B", Bronze="Player C")