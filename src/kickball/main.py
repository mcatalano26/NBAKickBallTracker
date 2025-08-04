from datetime import date

# from .db_updates import replace_season_dbs
# from .kickballs import update_kickball_db
# from .player_info import update_minutes_db
from .data_analysis import get_podium


def main():
    # relatively quick operation, can be done every time
    # replace_season_dbs()
    
    start_date = date(2025, 2, 1)
    end_date = date(2025, 2, 28)
    
    # Long operation...be careful before running
    # update_kickball_db(start_date, end_date)
    
    # Even longer than updating kickball db
    # update_minutes_db(start_date, end_date)
    
    podium = get_podium(start_date, end_date)
    print(podium)


if __name__ == "__main__":
    main()
