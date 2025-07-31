
import os

import git
from nba_api.stats.static import players, teams  # type: ignore


def get_git_root() -> str:
    git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root

def get_active_player_dict() -> dict[int, str]:
    """
    Returns:
        dict[int, str]: id to full name mapping of active players
    """
    return {p["id"]: p["full_name"] for p in players.get_players() if p["is_active"]}


def get_active_team_lst() -> list[str]:
    """
    Returns:
        list[str]: list of active team nicknames
    """
    nba_teams = teams.get_teams()
    return [team["abbreviation"] for team in nba_teams]

def get_team_id_from_abbr(abbr: str) -> int:
    """
    Args:
        name (str): Team name (i.e. "Lakers")

    Returns:
        int: Team ID or 0 if not found
    """
    nba_teams = teams.get_teams()
    for team in nba_teams:
        if team["abbreviation"] in get_active_team_lst():
            if team["abbreviation"] == abbr:
                return team["id"]
    return 0


def get_player_id(name: str) -> int:
    """
    Args:
        name (str): player name (i.e. "LeBron James")

    Returns:
        int: player id
    """
    nba_players = players.get_players()
    for player in nba_players:
        if player["full_name"] == name:
            return player["id"]
    return 0
