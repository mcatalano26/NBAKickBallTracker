import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from .data_analysis import Podium


def send_email(season_podium: Podium, month_podium: Podium, time_range: str, season: str, sender_email: str, sender_password: str, recipient_emails: List[str]):
    """
    Send a beautifully formatted email displaying the podium winners.
    
    Args:
        season_podium: Podium dataclass with Gold, Silver, Bronze players
        month_podium: Podium dataclass with Gold, Silver, Bronze players for the month
        recipient_emails: List of email addresses to send to
        subject: Email subject line
    """
    
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Kickball Leaderboards</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f4f6fb;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.08);
                overflow: hidden;
            }}
            .header {{
                background: #2d6cdf;
                color: #fff;
                text-align: center;
                padding: 32px 20px 20px 20px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2em;
                letter-spacing: 1px;
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 1.1em;
                opacity: 0.85;
            }}
            .section-title {{
                text-align: center;
                font-size: 1.3em;
                font-weight: bold;
                color: #2d6cdf;
                margin: 32px 0 12px 0;
                letter-spacing: 0.5px;
            }}
            .podium {{
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                gap: 16px;
                padding: 32px 20px;
            }}
            .place {{
                flex: 1;
                background: #f8f9fa;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                text-align: center;
                padding: 24px 10px 18px 10px;
                margin: 0 4px;
                transition: box-shadow 0.2s;
            }}
            .place:hover {{
                box-shadow: 0 6px 18px rgba(44,62,80,0.10);
            }}
            .medal {{
                font-size: 2.5em;
                margin-bottom: 10px;
                display: block;
            }}
            .place-title {{
                font-size: 1.1em;
                font-weight: 600;
                color: #2d6cdf;
                margin-bottom: 8px;
                letter-spacing: 0.5px;
            }}
            .player-name {{
                font-size: 1.25em;
                font-weight: bold;
                color: #222;
                margin-bottom: 12px;
            }}
            .stats {{
                background: #eaf0fa;
                border-radius: 8px;
                padding: 12px;
                margin-top: 10px;
                font-size: 1em;
            }}
            .stat-item {{
                display: flex;
                justify-content: space-between;
                margin: 6px 0;
                padding-bottom: 4px;
                border-bottom: 1px solid #dde3ec;
            }}
            .stat-item:last-child {{
                border-bottom: none;
            }}
            .stat-label {{
                color: #555;
                font-weight: 500;
            }}
            .stat-value {{
                font-weight: bold;
                color: #2d6cdf;
            }}
            .footer {{
                text-align: center;
                padding: 22px;
                background: #2d6cdf;
                color: #fff;
                font-size: 0.95em;
                border-radius: 0 0 12px 12px;
            }}
            @media (max-width: 700px) {{
                .podium {{
                    flex-direction: column;
                    align-items: stretch;
                }}
                .place {{
                    margin: 10px 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Kickball Leaderboards</h1>
                <p>{time_range} edition</p>
            </div>
            <div class="section-title">🏅 {time_range} Standings 🏅</div>
            <div class="podium">
                <!-- First Place -->
                <div class="place">
                    <span class="medal">🥇</span>
                    <div class="place-title">1st Place</div>
                    <div class="player-name">{month_podium.Gold.FullName}</div>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Total Kicks</span>
                            <span class="stat-value">{month_podium.Gold.TotalKicks}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Kicks/Min</span>
                            <span class="stat-value">{month_podium.Gold.KicksPerMinute:.3f}</span>
                        </div>
                    </div>
                </div>
                <!-- Second Place -->
                <div class="place">
                    <span class="medal">🥈</span>
                    <div class="place-title">2nd Place</div>
                    <div class="player-name">{month_podium.Silver.FullName}</div>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Total Kicks</span>
                            <span class="stat-value">{month_podium.Silver.TotalKicks}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Kicks/Min</span>
                            <span class="stat-value">{month_podium.Silver.KicksPerMinute:.3f}</span>
                        </div>
                    </div>
                </div>
                <!-- Third Place -->
                <div class="place">
                    <span class="medal">🥉</span>
                    <div class="place-title">3rd Place</div>
                    <div class="player-name">{month_podium.Bronze.FullName}</div>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Total Kicks</span>
                            <span class="stat-value">{month_podium.Bronze.TotalKicks}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Kicks/Min</span>
                            <span class="stat-value">{month_podium.Bronze.KicksPerMinute:.3f}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="section-title">🏅 Season Standings 🏅</div>
            <div class="podium">
                <!-- First Place -->
                <div class="place">
                    <span class="medal">🥇</span>
                    <div class="place-title">1st Place</div>
                    <div class="player-name">{season_podium.Gold.FullName}</div>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Total Kicks</span>
                            <span class="stat-value">{season_podium.Gold.TotalKicks}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Kicks/Min</span>
                            <span class="stat-value">{season_podium.Gold.KicksPerMinute:.3f}</span>
                        </div>
                    </div>
                </div>
                <!-- Second Place -->
                <div class="place">
                    <span class="medal">🥈</span>
                    <div class="place-title">2nd Place</div>
                    <div class="player-name">{season_podium.Silver.FullName}</div>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Total Kicks</span>
                            <span class="stat-value">{season_podium.Silver.TotalKicks}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Kicks/Min</span>
                            <span class="stat-value">{season_podium.Silver.KicksPerMinute:.3f}</span>
                        </div>
                    </div>
                </div>
                <!-- Third Place -->
                <div class="place">
                    <span class="medal">🥉</span>
                    <div class="place-title">3rd Place</div>
                    <div class="player-name">{season_podium.Bronze.FullName}</div>
                    <div class="stats">
                        <div class="stat-item">
                            <span class="stat-label">Total Kicks</span>
                            <span class="stat-value">{season_podium.Bronze.TotalKicks}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Kicks/Min</span>
                            <span class="stat-value">{season_podium.Bronze.KicksPerMinute:.3f}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">
                <em>Recognizing elite ball-kicking talent</em><br>
                <span style="opacity:0.8;">For Mangos eyes only 👀🥭</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🏀 {season} Kickball Leaderboard 🏆"
    msg["From"] = f"Kickin' Balls <{sender_email}>"
    msg["To"] = ", ".join(recipient_emails)
    
    # Add HTML content
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)
    
    try:
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✅ Podium email sent successfully to {len(recipient_emails)} recipients")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise