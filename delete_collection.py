import os
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

batch_size = 500

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0
    for doc in docs:
        print(f"Deleting doc {doc.id}")
        doc.reference.delete()
        deleted += 1
    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

if __name__ == "__main__":
    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    coll_ref = db.collection(COLLECTION_NAME)
    delete_collection(coll_ref, batch_size)
    print(f"Collection '{COLLECTION_NAME}' deletion complete.") 