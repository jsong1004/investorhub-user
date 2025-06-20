# This script sends email reminders to event attendees using SendGrid API.
# Note: SendGrid has a free tier limitation of 100 emails per day.
# If you need to send more emails, consider upgrading to a paid plan or using a different email service.
# The script reads attendee information from Firestore and sends personalized reminders
# with event details, parking information, and a link to the check-in/voting portal.

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
        <p>This is a reminder that the Startup World Cup Seattle Regional event is happening today, from 5:00 PM to 8:30 PM, for an evening of innovation!</p>
        <p>We're excited to host you at the University of Washington's Kane Auditorium (Kane Hall).</p>
        <b>Parking Information:</b>
        <ul>
            <li><b>The closest and most convenient parking for Kane Hall is the Central Plaza Parking Garage (CPG).</b></li>
            <li><b>Entrance:</b> Via NE 41st St, just off 15th Ave NE.</li>
            <li><b>Parking Rates:</b> Flat rate after 4 PM (approximately $13).</li>
            <li><b>Payment:</b> You can pay at the gatehouse or use PayByPhone (Location ID: 123211).</li>
            <li><b>Accessibility:</b> An elevator in the northeast corner of the garage brings you directly to Red Square, just a few steps from Kane Hall.</li>
        </ul>
<p>To ensure a smooth experience and to participate fully in the event, please use your personalized event portal to check in upon arrival and to vote for your favorite startups! </p>
<p><b> Check In and Voting Portal:</b><p><p><a href='{personal_link}'>{personal_link}</a></p><p>Your vote matters for our special <b>"Audience Choice Awards"</b> – support and cheer for your favorite startup</p>
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