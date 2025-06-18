import os
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

EXCLUDE_EMAILS = {"jsong@koreatous.com", "jsong@seattlepartners.us"}
BATCH_SIZE = 500

def delete_except_emails(coll_ref, exclude_emails, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0
    for doc in docs:
        data = doc.to_dict()
        email = data.get("email") or data.get("Email")
        if email not in exclude_emails:
            print(f"Deleting doc {doc.id} ({email})")
            doc.reference.delete()
            deleted += 1
        else:
            print(f"Skipping doc {doc.id} ({email})")
    if deleted >= batch_size:
        return delete_except_emails(coll_ref, exclude_emails, batch_size)

if __name__ == "__main__":
    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    coll_ref = db.collection(COLLECTION_NAME)
    delete_except_emails(coll_ref, EXCLUDE_EMAILS, BATCH_SIZE)
    print("Selective deletion complete.") 