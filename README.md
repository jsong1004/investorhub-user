# Investor Hub Firestore Utilities

This repository contains Python scripts to manage guest data for the Startup World Cup Seattle Regional event, including importing guests, updating their information, handling check-ins, managing votes for startups, and collecting event feedback.

## Features
- **`import-guests.py`**: Imports guest data from a CSV file stored in a Google Cloud Storage (GCS) bucket into a Firestore collection.
- **`update-guests.py`**: Updates specific guest documents in Firestore based on a unique identifier like email.
- **`add-checkin.py`**: Adds a default `check_in` field to all documents in the guest collection, useful for initialization.
- **`generate-qrcodes.py`**: Generates unique QR codes for each guest, linking them to their personalized user portal page for easy access.
- **`server.py`**: A Flask web application that serves the user portal, handles guest check-ins via QR code scans, processes startup votes, and collects event feedback.
- **User Portal (`/user_portal`)**: A personalized page for each guest to check in, vote for startups, and provide event feedback. The links dynamically disable once the action is completed.
- **Vote for Startup Page (`/vote`)**: Allows guests to vote for their favorite startups across different categories (Most Inspiring Pitch, Crowd Favorite, Most Innovative Idea).
- **Event Feedback Page (`/feedback`)**: Collects valuable feedback from guests about their event experience.

## Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd investor-hub
```

### 2. Create a Virtual Environment (Recommended)
```bash
python3 -m venv investor-hub
source investor-hub/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Google Cloud Project Setup
Ensure you have a Google Cloud Project with Firestore and Cloud Storage enabled.

### 5. Set Up Environment Variables
Create a `.env` file in the project root with the following content. Replace placeholders with your actual Google Cloud details:

```
PROJECT_ID=myresume-457817
DATABASE_ID=investorhub
COLLECTION_NAME=Startup-World-Cup-Seattle-Regional-Guests
BUCKET_NAME=investor-hub
CSV_FILE_NAME=Startup-World-Cup-Seattle-Regional-Guests.csv
USER_PORTAL_BASE_URL=https://<YOUR_CLOUD_RUN_SERVICE_URL_OR_LOCAL_HOST>
```
**Note:** `<YOUR_CLOUD_RUN_SERVICE_URL_OR_LOCAL_HOST>` should be updated after your first Cloud Run deployment or set to `http://localhost:5000` for local testing.

### 6. Google Cloud Authentication

**For Local Development:**
Make sure you have authenticated with Google Cloud and have the necessary permissions. The recommended way is to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your service account JSON key file:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
```

**For Cloud Build / Cloud Run Deployment:**
Your service account key should be stored securely in Google Cloud Secret Manager.

1.  **Create Secret:** Store the content of your service account JSON key file in Secret Manager. Name the secret `ServiceAccountKey` (or your preferred name) in project `myresume-457817`.
    ```bash
    gcloud secrets create ServiceAccountKey --data-file=/path/to/your/service-account-key.json --project=myresume-457817
    ```
2.  **Grant Permissions:**
    *   **Cloud Build Service Account** (`[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com`): Needs `Secret Manager Secret Accessor`, `Cloud Run Admin`, `Service Account User`, and `Storage Object Admin` roles.
    *   **Cloud Run Runtime Service Account** (default: `myresume-457817@appspot.gserviceaccount.com`): Needs `Cloud Datastore User`, `Cloud Storage Object Viewer`, or `Firebase Firestore User` roles to access Firestore and GCS data.

## Usage

### Run the Web Server (Local Development)
To run the Flask application locally:
```bash
python server.py
```
Access the user portal at: `http://localhost:5000/user_portal?email=your-email@example.com`

### Generate QR Codes
To generate QR codes for all guests. The QR codes will point to their respective user portal pages.
```bash
python generate-qrcodes.py
```
QR codes will be saved in the `qrcodes/` directory.

### Import Guests from CSV to Firestore
To import initial guest data from a CSV file in GCS:
```bash
python import-guests.py
```

### Update a Guest Document in Firestore
To manually update a specific guest's document (e.g., change `UNIQUE_IDENTIFIER_VALUE` in the script):
```bash
python update-guests.py
```

### Add Check-in Field to All Documents
To initialize a `check_in` field for all existing documents (if not already present):
```bash
python add-checkin.py
```

## Deployment to Google Cloud Run (Automated via Cloud Build)

This project includes a `cloudbuild.yaml` for automated deployment to Google Cloud Run.

1.  **Configure `USER_PORTAL_BASE_URL` in `.env` (Locally) and `cloudbuild.yaml` (for Cloud Run):** Update the `USER_PORTAL_BASE_URL` with your Cloud Run service URL after its first deployment.
2.  **Trigger Cloud Build:** From your project root, run the following command. This will build your Docker image, push it to Google Container Registry (GCR), and deploy it to Cloud Run.
    ```bash
    gcloud builds submit --config cloudbuild.yaml .
    ```

## Notes
- All scripts and the web server use environment variables for configuration.
- Ensure your service accounts (local, Cloud Build, Cloud Run runtime) have the necessary IAM permissions for Firestore, GCS, and Secret Manager.

## License
MIT 
MIT 