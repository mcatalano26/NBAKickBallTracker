import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd  # type: ignore

from .utils import get_games_for_date_range, get_git_root


@dataclass
class Player:
    FullName: str
    TotalKicks: int
    KicksPerMinute: float

@dataclass
class Podium:
    Gold: Player
    Silver: Player
    Bronze: Player
 

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

def make_time_delta(entry):
    m, s = entry.split(':')
    return timedelta(hours=0, minutes=int(m), seconds=int(s))

def get_podium(start_date: date, end_date: date) -> Podium:
    game_ids = get_games_for_date_range(start_date, end_date)
    
    minutes_df = get_game_range_df(game_ids, "minutes")
    kick_df = get_game_range_df(game_ids, "kickballs")
    players_df = get_df("players")
    
    # Modify minutes_df to be total minutes per player. Only need playerId and minutes columns
    minutes_df = minutes_df[["personId", "minutes"]]

    minutes_df["minutes"] = minutes_df["minutes"].apply(lambda entry: make_time_delta(entry))
    minutes_df = minutes_df.groupby("personId")["minutes"].sum().reset_index()
    minutes_df = minutes_df.rename(columns={"minutes": "total_minutes"})
    
    # Modify kick_df to be total kicks per player. Only need personId and a kicks column
    kick_df = kick_df[["personId"]]
    kick_df = kick_df.groupby("personId").agg(total_kicks=("personId", "count")).reset_index()
    
    # Merge these two dataframes on personId
    final_df = pd.merge(minutes_df, kick_df, on="personId", how="left").dropna(subset=["total_kicks"]).reset_index(drop=True)
    final_df["kpm"] = final_df["total_kicks"] / final_df["total_minutes"].dt.total_seconds() * 60
    
    players_df = players_df.rename(columns={"id": "personId"})
    final_df = pd.merge(final_df, players_df, on="personId", how="left")
    final_df["full_name"] = final_df["first_name"] + " " + final_df["last_name"]
    final_df = final_df[["full_name", "total_kicks", "kpm"]]
    final_df = final_df.sort_values(by=["total_kicks", "kpm"], ascending=False).reset_index(drop=True)
    
    return Podium(Gold=Player(FullName=final_df["full_name"].loc[0], TotalKicks=int(final_df["total_kicks"].loc[0]), KicksPerMinute=round(float(final_df["kpm"].loc[0]), 4)),
                  Silver=Player(FullName=final_df["full_name"].loc[1], TotalKicks=int(final_df["total_kicks"].loc[1]),KicksPerMinute=round(float(final_df["kpm"].loc[1]), 4)),
                  Bronze=Player(FullName=final_df["full_name"].loc[2], TotalKicks=int(final_df["total_kicks"].loc[2]), KicksPerMinute=round(float(final_df["kpm"].loc[2]), 4))
                )