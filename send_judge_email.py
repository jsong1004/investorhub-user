import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables from .env file
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
USER_PORTAL_BASE_URL = os.getenv("USER_PORTAL_BASE_URL", "https://investorhub.ai-biz.app")

JUDGE_EMAILS = [
    "kotzermark@gmail.com",
    "ron@venturemechanics.com",
    "gm@kscseattle.org",
    "angie@allianceofangels.com",
    "jesse@dreamward.vc",
    "vtrask@gmail.com",
    "lvreed@hey.com",
    "Ian.Hameroff@fulcrum.group",
    "jp@shucker.vc",
    "Gabe.Regalado@nmrk.com",
    "jsong@seattlepartners.us"
]

def send_judge_email(email):
    name = "Judge"
    personal_link = f"{USER_PORTAL_BASE_URL}?email={email}"
    message = Mail(
        from_email=ADMIN_EMAIL,
        to_emails=email,
        subject="Startup World Cup Seattle Regional - Startup Pitch Scoring Platform",
        html_content=f"""
        <p>Hi {name},</p>
        <p>Thank you for dedicating your valuable time to judge the Startup World Cup Seattle Regional! We truly appreciate your contribution to this event and the entrepreneurial community.</p>
        <p>Just a reminder, the event takes place tomorrow, Wednesday, June 18, 2025, from 5:00 PM to 8:30 PM at the University of Washington's Kane Auditorium. We're looking forward to an insightful evening of pitches.</p>
        <b style='color:#1a73e8;'>Startup Pitch Scoring Platform</b>
        <p>To facilitate the judging process, we'll be utilizing our personalized event portal. This platform will allow you to efficiently score each startup's pitch.</p>
        <p>You can access your personalized portal here: <a href='{personal_link}'>{personal_link}</a></p>
        <b>Looking Forward to Tomorrow</b>
        <p>Thank you once again for your expertise and time. Your insights are crucial to the success of these promising startups. We look forward to seeing you tomorrow!</p>
        <p>Sincerely,<br>The Startup World Cup Seattle Regional Team</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Sent judge reminder to {email} (status: {response.status_code})")
    except Exception as e:
        print(f"Failed to send to {email}: {e}")

def main():
    # Handle SSL certificate issues in corporate environments
    import ssl
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    for email in JUDGE_EMAILS:
        send_judge_email(email)

if __name__ == "__main__":
    main() 