
import sqlite3

import numpy as np
import pandas as pd  # type: ignore
from nba_api.stats.endpoints import leaguegamefinder  # type: ignore
from nba_api.stats.library.parameters import Season, SeasonType  # type: ignore
from nba_api.stats.static import players  # type: ignore
from sqlalchemy import create_engine  # type: ignore

from .utils import get_active_team_lst, get_git_root, get_team_id_from_abbr


def df_to_db(df: pd.DataFrame, db_name: str, if_exists_method: str) -> None:
    db = create_engine(f"sqlite:////{get_git_root()}/data/{db_name}.db")
    
    if if_exists_method == "replace":
        df.to_sql(f"{db_name}", db, if_exists=if_exists_method, index=False)
    elif if_exists_method == "append":
        with sqlite3.connect(f"{get_git_root()}/data/{db_name}.db") as conn:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                columns = ", ".join(row.index)
                placeholders = ", ".join(["?"] * len(row))
                sql = f"INSERT OR IGNORE INTO {db_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(row.values))
    else:
        raise ValueError("if_exists_method must be either 'replace' or 'append'")
    

def replace_players_db() -> None:
    nba_players = players.get_players()
    
    nba_players_df = pd.DataFrame(nba_players)
    
    nba_players_df = nba_players_df[["id", "first_name", "last_name", "is_active"]]
    
    df_to_db(nba_players_df, "players", "replace")
    
    print("players database updated successfully.")

def replace_teams_db(games_df: pd.DataFrame) -> None:
    teams_df = games_df[["TEAM_ID", "TEAM_ABBREVIATION", "TEAM_NAME"]].drop_duplicates().reset_index(drop=True)

    df_to_db(teams_df, "teams", "replace")
    
    print("teams database updated successfully.")

def replace_games_db(games_df: pd.DataFrame) -> None:
    games_df = games_df[["GAME_ID", "MATCHUP", "GAME_DATE"]]
    games_df = games_df.drop_duplicates(subset=["GAME_ID"], keep='first').reset_index(drop=True)
    
    games_df["HOME_TEAM_ABBR"] = np.where(
        games_df["MATCHUP"].str.contains(" @ "),
        games_df["MATCHUP"].str.split(" @ ").str[1],
        games_df["MATCHUP"].str.split(" vs. ").str[0],
    )
    
    games_df["AWAY_TEAM_ABBR"] = np.where(
        games_df["MATCHUP"].str.contains(" @ "),
        games_df["MATCHUP"].str.split(" @ ").str[0],
        games_df["MATCHUP"].str.split(" vs. ").str[1],
    )
    
    games_df["HOME_TEAM_ID"] = games_df["HOME_TEAM_ABBR"].apply(get_team_id_from_abbr)
    games_df["AWAY_TEAM_ID"] = games_df["AWAY_TEAM_ABBR"].apply(get_team_id_from_abbr)
    
    games_df = games_df.drop(columns=["MATCHUP"])
    
    df_to_db(games_df, "games", "replace")
    
    print("games database updated successfully.")
    
    
def replace_season_dbs() -> None:
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=Season.default, season_type_nullable=SeasonType.regular)
    
    games_dict = gamefinder.get_normalized_dict()
    games = games_dict["LeagueGameFinderResults"]
    
    games_df = pd.DataFrame(games)
    
    active_nba_team_ids = [get_team_id_from_abbr(team) for team in get_active_team_lst()]
    games_df = games_df[games_df["TEAM_ID"].isin(active_nba_team_ids)]
    
    replace_games_db(games_df)
    replace_teams_db(games_df)
    replace_players_db()