import pandas as pd
from google.cloud import firestore
from google.cloud import storage
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Your Google Cloud Details ---
PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
CSV_FILE_NAME = os.getenv("CSV_FILE_NAME")

# --- Firestore Collection ---
# IMPORTANT: Change this to the name of the collection you want to create/use.
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def import_csv_to_firestore(event=None, context=None):
    """
    Reads a CSV file from Google Cloud Storage and imports each row into a Firestore collection.
    """
    print(f"Starting Firestore import process for project '{PROJECT_ID}'...")

    try:
        # Initialize clients
        # The db client must be initialized with the specific database ID
        db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
        storage_client = storage.Client(project=PROJECT_ID)

        # Get the CSV file from GCS
        print(f"Fetching '{CSV_FILE_NAME}' from bucket '{BUCKET_NAME}'...")
        bucket = storage_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(CSV_FILE_NAME)
        
        # Download the contents of the blob as a string
        csv_data = blob.download_as_text()
        
        # Use pandas to read the CSV data from the string
        # The `io.StringIO` wrapper makes the string behave like a file
        df = pd.read_csv(io.StringIO(csv_data))

        # Check if the dataframe is empty
        if df.empty:
            print("CSV file is empty. No data to import.")
            return

        print(f"CSV file loaded successfully. Found {len(df)} rows to import into collection '{COLLECTION_NAME}'.")

        # Iterate over each row in the dataframe and add it to Firestore
        for index, row in df.iterrows():
            # Convert row to a dictionary, handling potential NaN values
            # Pandas can sometimes read empty cells as NaN (Not a Number), which Firestore can't store.
            # We convert them to None, which Firestore can handle.
            doc_data = row.where(pd.notna(row), None).to_dict()
            
            # Add a new document to the specified collection.
            # Firestore will auto-generate an ID for each new document.
            db.collection(COLLECTION_NAME).add(doc_data)
            print(f"  > Imported row {index + 1}...")

        print("\n✅ Firestore import completed successfully!")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_NAME}' was not found in the bucket '{BUCKET_NAME}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- To run the script directly from your computer ---
if __name__ == "__main__":
    import_csv_to_firestore()