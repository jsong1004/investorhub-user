import os
import ssl
from google.cloud import firestore
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
USER_PORTAL_BASE_URL = os.getenv("USER_PORTAL_BASE_URL", "https://investorhub-user.ai-biz.app/user_portal")


def send_reminder_email(name, email):
    personal_link = f"{USER_PORTAL_BASE_URL}?email={email}"
    message = Mail(
        from_email=ADMIN_EMAIL,
        to_emails=email,
        subject="Event Reminder - Startup World Cup Seattle Regional",
        html_content=f"""
        <p>Hi {name},</p>
        <p>This is a reminder that the Startup World Cup Seattle Regional event is just one day away! Join us tomorrow, Wednesday, June 18th, from 5:00 PM to 8:30 PM for an evening of innovation.</p>
        <p>We're excited to host you at the University of Washington's Kane Auditorium.</p>
        <p><b style='color:#1a73e8;'>To ensure a smooth experience, please use your personalized event portal to check in and cast your votes for the competing startups:</b></p>
        <p><a href='{personal_link}'>{personal_link}</a></p>
        <p>We look forward to seeing you there and appreciate your support for the entrepreneurial community!</p>
        <p>Sincerely,<br>The Startup World Cup Seattle Regional Team</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Sent reminder to {email} (status: {response.status_code})")
    except Exception as e:
        print(f"Failed to send to {email}: {e}")


def main():
    # Handle SSL certificate issues in corporate environments
    try:
        # Try to create unverified SSL context as fallback
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    
    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    guests_ref = db.collection(COLLECTION_NAME)
    guests = guests_ref.stream()
    for guest in guests:
        data = guest.to_dict()
        name = data.get("name") or data.get("Name") or data.get("full_name") or "there"
        email = data.get("email") or data.get("Email")
        if email:
            send_reminder_email(name, email)
        else:
            print(f"Skipping guest with missing email: {data}")

if __name__ == "__main__":
    main() 