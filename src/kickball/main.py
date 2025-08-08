import os
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
from nba_api.stats.library.parameters import Season  # type: ignore

from .data_analysis import get_podium
from .db_updates import replace_season_dbs
from .email import send_email
from .kickballs import update_kickball_db
from .player_info import update_minutes_db


def get_dates():
    
    return (date(2025, 4, 1), date(2025, 4, 1), date(2025, 4, 1), "April")
    
    # This will be run on the first of every month
    yesterday = datetime.now() - timedelta(days=1)
    last_month_name = yesterday.strftime("%B")
    
    # TODO: Use nba_api to get the current season actual start date
    # Hardcoding 2025-26 season start date for now
    season_start_date = date(2025, 10, 21)
    
    month_start_date = date(yesterday.year, yesterday.month, 1)
    month_end_date = date(yesterday.year, yesterday.month, yesterday.day)
    
    return season_start_date, month_start_date, month_end_date, last_month_name

def get_podiums(season_start_date, month_start_date, month_end_date):
    # relatively quick operation, can be done every time
    replace_season_dbs()
    
    # Long operation...be careful before running
    update_kickball_db(month_start_date, month_end_date)
    
    # Even longer than updating kickball db
    update_minutes_db(month_start_date, month_end_date)
    
    season_podium = get_podium(season_start_date, month_end_date)
    month_podium = get_podium(month_start_date, month_end_date)
    
    return season_podium, month_podium

def send_kickball_email(season_podium, month_podium, last_month_name):
    load_dotenv()
    
    sender_email = "thekickballtracker@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_emails = ["mattcat26@gmail.com"]
    
    season = Season.default
    
    send_email(season_podium, month_podium, last_month_name, season, sender_email, sender_password, recipient_emails)


def main():
    season_start_date, month_start_date, month_end_date, last_month_name = get_dates()
        
    season_podium, month_podium = get_podiums(season_start_date, month_start_date, month_end_date)
    
    send_kickball_email(season_podium, month_podium, last_month_name)


if __name__ == "__main__":
    main()
