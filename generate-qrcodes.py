import os
from dotenv import load_dotenv
from google.cloud import firestore
import qrcode

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Set this to your deployed user portal URL
USER_PORTAL_BASE_URL = os.getenv("USER_PORTAL_BASE_URL", "https://investorhub-user.ai-biz.app/user_portal")

OUTPUT_DIR = "qrcodes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(email):
    return email.replace("@", "_at_").replace(".", "_dot_")

def generate_qrcodes():
    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    collection_ref = db.collection(COLLECTION_NAME)
    docs = collection_ref.stream()
    count = 0
    for doc in docs:
        data = doc.to_dict()
        email = data.get("email")
        if not email:
            print(f"Skipping document {doc.id}: no email field.")
            continue
        # Generate QR code pointing to user portal
        user_portal_url = f"{USER_PORTAL_BASE_URL}?email={email}"
        img = qrcode.make(user_portal_url)
        filename = os.path.join(OUTPUT_DIR, f"qrcode_{sanitize_filename(email)}.png")
        img.save(filename)
        print(f"Generated QR code for {email}: {filename}")
        count += 1
    print(f"\n✅ Generated {count} QR codes in '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    generate_qrcodes() 