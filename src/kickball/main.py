import os
from datetime import date

from dotenv import load_dotenv

# from .db_updates import replace_season_dbs
# from .kickballs import update_kickball_db
# from .player_info import update_minutes_db
from .data_analysis import get_podium
from .email import send_email


def main():
    # relatively quick operation, can be done every time
    # replace_season_dbs()
    
    season_start_date = date(2025, 2, 1)
    season_end_date = date(2025, 2, 28)
    
    month_start_date = date(2025, 2, 1)
    month_end_date = date(2025, 2, 15)
    
    # Long operation...be careful before running
    # update_kickball_db(start_date, end_date)
    
    # Even longer than updating kickball db
    # update_minutes_db(start_date, end_date)
    
    season_podium = get_podium(season_start_date, season_end_date)
    month_podium = get_podium(month_start_date, month_end_date)
    
    load_dotenv()
    
    sender_email = "thekickballtracker@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_emails = ["mattcat26@gmail.com"]
    month = "February"
    season = "2024-2025"
    
    send_email(season_podium, month_podium, month, season, sender_email, sender_password, recipient_emails)


if __name__ == "__main__":
    main()
