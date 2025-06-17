import os
from dotenv import load_dotenv
from google.cloud import firestore

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

DEFAULT_CHECKIN_VALUE = 0


def add_checkin_to_all_documents():
    print(f"Adding 'check_in' field with default value {DEFAULT_CHECKIN_VALUE} to all documents in '{COLLECTION_NAME}'...")
    try:
        db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
        collection_ref = db.collection(COLLECTION_NAME)
        docs = collection_ref.stream()
        updated_count = 0
        for doc in docs:
            doc_ref = doc.reference
            doc_ref.update({"check_in": DEFAULT_CHECKIN_VALUE})
            print(f"  > Updated document ID: {doc.id}")
            updated_count += 1
        print(f"\n✅ Added 'check_in' field to {updated_count} documents in '{COLLECTION_NAME}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    add_checkin_to_all_documents() 