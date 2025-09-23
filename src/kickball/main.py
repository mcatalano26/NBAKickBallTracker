import os
import sys
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
from nba_api.stats.library.parameters import Season  # type: ignore

from .data_analysis import get_podium
from .db_updates import replace_season_dbs
from .email import send_email
from .kickballs import update_kickball_db
from .player_info import update_minutes_db

SEASON_START_DATE = date(2025, 10, 21)

def get_podiums(season_start_date, start_date, end_date):
    # relatively quick operation, can be done every time
    replace_season_dbs()
    
    # Long operation...be careful before running
    update_kickball_db(start_date, end_date)
    
    # Even longer than updating kickball db
    update_minutes_db(start_date, end_date)
    
    season_podium = get_podium(season_start_date, end_date)
    month_podium = get_podium(start_date, end_date)
    
    return season_podium, month_podium

def send_kickball_email(season_podium, month_podium, time_range):
    load_dotenv()
    
    sender_email = "thekickballtracker@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_emails = ["mattcat26@gmail.com"]
    
    season = Season.default
    
    send_email(season_podium, month_podium, time_range, season, sender_email, sender_password, recipient_emails)

# Must run on the first of every month
def monthly_cron_job():
    yesterday = datetime.now() - timedelta(days=1)
    last_month_name = yesterday.strftime("%B")
    month_start_date = date(yesterday.year, yesterday.month, 1)
    month_end_date = date(yesterday.year, yesterday.month, yesterday.day)
        
    season_podium, month_podium = get_podiums(SEASON_START_DATE, month_start_date, month_end_date)
    
    send_kickball_email(season_podium, month_podium, last_month_name)
   
# Should send an email on Sunday morning for the games from Sunday-Saturday of the prior week
def weekly_cron_job():
    week_start_date = datetime.now() - timedelta(days=7)
    week_end_date = datetime.now() - timedelta(days=1)

    last_week_name = f"{week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d')}" 
    
    ### TEST ONLY ###
    week_start_date = date(2025, 4, 1)
    week_end_date = date(2025, 4, 1)
    SEASON_START_DATE = date(2025, 4, 1)
    ### TEST ONLY ###    
    
    season_podium, week_podium = get_podiums(SEASON_START_DATE, week_start_date, week_end_date)
    
    send_kickball_email(season_podium, week_podium, last_week_name)
    
def test():
    print("Running test")
    sys.exit(0)
    
# To run, execute `uv run -m kickball.main (weekly|monthly)` from the src directory
if __name__ == "__main__":
    if len(sys.argv) < 2:
        test()

    param = sys.argv[1]

    if param == "weekly":
        weekly_cron_job()
    elif param == "monthly":
        monthly_cron_job()
    else:
        test()
