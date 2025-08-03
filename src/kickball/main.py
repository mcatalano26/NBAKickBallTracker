from datetime import date

from .db_updates import replace_season_dbs
from .kickballs import update_kickball_db
from .player_info import update_minutes_db


def main():
    replace_season_dbs()
    
    start_date = date(2025, 3, 1)
    end_date = date(2025, 3, 1)
    
    update_kickball_db(start_date, end_date)
    
    update_minutes_db(start_date, end_date)


if __name__ == "__main__":
    main()
