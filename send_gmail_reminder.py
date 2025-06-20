# This script sends email reminders to event attendees using Gmail SMTP.
# Note: Gmail has a sending limit of 500 emails per day for free accounts.
# If you need to send more emails, consider using a different email service.
import os
import ssl
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password for Gmail
USER_PORTAL_BASE_URL = os.getenv("USER_PORTAL_BASE_URL", "https://investorhub-user.ai-biz.app/user_portal")

# Replace this list with your actual (name, email) pairs
PEOPLE = [

    ("Jae Rhee", "jaerhee@uw.edu")
]

def send_reminder_email(name, email):
    personal_link = f"{USER_PORTAL_BASE_URL}?email={email}"
    html_content = f"""
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
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Event Reminder - Startup World Cup Seattle Regional"
    msg.attach(MIMEText(html_content, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Sent reminder to {email}")
    except Exception as e:
        print(f"Failed to send to {email}: {e}")

def main():
    for name, email in PEOPLE:
        send_reminder_email(name, email)

if __name__ == "__main__":
    main() 