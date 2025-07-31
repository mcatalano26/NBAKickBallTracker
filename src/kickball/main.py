
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from nba_api.stats.endpoints import leaguegamefinder  # type: ignore
from nba_api.stats.library.parameters import Season, SeasonType  # type: ignore
from sqlalchemy import create_engine  # type: ignore

from .utils import get_active_team_lst, get_git_root, get_team_id_from_abbr


def main():
    
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=Season.default, season_type_nullable=SeasonType.regular)
    
    games_dict = gamefinder.get_normalized_dict()
    games = games_dict["LeagueGameFinderResults"]
    
    games_df = pd.DataFrame(games)
    
    active_nba_team_ids = [get_team_id_from_abbr(team) for team in get_active_team_lst()]
    print(active_nba_team_ids)
    games_df = games_df[games_df["TEAM_ID"].isin(active_nba_team_ids)]
    
    teams_df = games_df[["TEAM_ID", "TEAM_ABBREVIATION", "TEAM_NAME"]].drop_duplicates().reset_index(drop=True)
    
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
    
    games_db = create_engine(f"sqlite:////{get_git_root()}/data/games.db")
    games_df.to_sql("games_db", games_db, if_exists="replace", index=False)
    
    teams_db = create_engine(f"sqlite:////{get_git_root()}/data/teams.db")
    teams_df.to_sql("teams_db", teams_db, if_exists="replace", index=False)
    
    print("all done for now")


if __name__ == "__main__":
    main()
