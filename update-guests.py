from google.cloud import firestore
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Your Google Cloud Details (now from environment variables) ---
PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# --- The Document to Update ---
# We will find the document where the 'Email' field matches this value.
# IMPORTANT: Make sure this field name ('Email') matches the column header in your original CSV.
UNIQUE_IDENTIFIER_FIELD = "email" 
UNIQUE_IDENTIFIER_VALUE = "jsong@koreatous.com" # <-- Change this to the email of the guest you want to update

# --- The New Data to Add ---
DATA_TO_ADD = {
    'vote': 1,
    'event_feedback': 'Excellent presentation, very insightful!'
}

def update_document():
    """Finds a document by a unique field and updates it with new data."""
    print(f"Attempting to update document in collection '{COLLECTION_NAME}'...")
    
    try:
        # Initialize Firestore client for the specific database
        db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
        
        # Get a reference to the collection
        collection_ref = db.collection(COLLECTION_NAME)
        
        # Query for the document based on the unique identifier
        query = collection_ref.where(
            field_path=UNIQUE_IDENTIFIER_FIELD, 
            op_string="==", 
            value=UNIQUE_IDENTIFIER_VALUE
        ).limit(1) # Use limit(1) as we expect only one result

        # Execute the query
        docs = query.stream()

        # Find the document and update it
        doc_found = False
        for doc in docs:
            doc_found = True
            print(f"  > Document found with ID: {doc.id}")
            print(f"  > Document data: {doc.to_dict()}")
            print(f"  > Applying update...")
            doc.reference.update(DATA_TO_ADD)
            print(f"  > Successfully added/updated fields: {list(DATA_TO_ADD.keys())}")

        if not doc_found:
            print(f"Error: No document found where '{UNIQUE_IDENTIFIER_FIELD}' is '{UNIQUE_IDENTIFIER_VALUE}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_document()