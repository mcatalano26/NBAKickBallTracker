from .db_updates import replace_season_dbs
from .kickballs import update_kickball_db


def main():
    replace_season_dbs()
    
    update_kickball_db()


if __name__ == "__main__":
    main()
