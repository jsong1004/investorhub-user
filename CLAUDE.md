# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an event management system for the Startup World Cup Seattle Regional, built with Flask and Google Cloud services. The system manages guest data, QR code generation, check-ins, voting, and feedback collection using Firestore as the database and Cloud Storage for CSV imports.

## Architecture
- **Flask Web Application** (`server.py`): Main web server with 7 routes handling user portal, check-ins, voting, and feedback
- **Guest Management Scripts**: Python utilities for importing, updating, and managing guest data
- **Google Cloud Integration**: Uses Firestore for data storage, Cloud Storage for CSV files, and Secret Manager for credentials
- **QR Code System**: Generates unique QR codes linking to personalized user portal pages
- **Deployment**: Containerized with Docker and deployed to Google Cloud Run via Cloud Build

## Key Components
- **User Portal** (`/user_portal`): Personalized pages for guests accessed via QR codes with dynamic button states
- **Three Core Functions**: Check-in, startup voting (3 categories), and event feedback
- **Data Collections**: 
  - Main guest collection: `Startup-World-Cup-Seattle-Regional-Guests`
  - Votes collection: `Startup-World-Cup-Seattle-Regional-Votes`
  - Feedback collection: `Startup-World-Cup-Seattle-Regional-Feedback`
- **Voting Categories**: Most Inspiring Pitch, Most Investable Startup, Most Innovative Idea
- **Companies**: Hardcoded list of 10 companies in `server.py:17-28`

## Environment Configuration
The application uses environment variables loaded from `.env` file:
- `PROJECT_ID`: Google Cloud project ID
- `DATABASE_ID`: Firestore database ID
- `COLLECTION_NAME`: Main guest collection name
- `BUCKET_NAME`: Cloud Storage bucket name
- `CSV_FILE_NAME`: Guest data CSV file name
- `USER_PORTAL_BASE_URL`: Base URL for user portal links

## Development Commands

### Local Development
```bash
# Set up virtual environment
python3 -m venv investor-hub
source investor-hub/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server locally
python server.py
```

### Data Management
```bash
# Import guest data from CSV in Cloud Storage
python import-guests.py

# Update specific guest documents
python update-guests.py

# Add check-in field to all documents
python add-checkin.py

# Generate QR codes for all guests
python generate-qrcodes.py

# Send reminder emails
python send_reminder.py

# Delete entire collection (use with caution)
python delete_collection.py

# Delete all documents except specific ones
python delete_except.py
```

### Deployment
```bash
# Deploy to Google Cloud Run via Cloud Build
gcloud builds submit --config cloudbuild.yaml .
```

## Authentication
- **Local Development**: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to service account key path
- **Cloud Deployment**: Service account key stored in Google Cloud Secret Manager as `ServiceAccountKey`

## Data Flow & State Management
- **User Portal State**: Dynamic button enabling/disabling based on Firestore document existence
- **Duplicate Prevention**: All submissions check for existing documents before creating new ones
- **Status Messages**: Context-aware messages based on completion state combinations
- **Email-based Document Keys**: All collections use email as document ID for consistent lookups

## Template Structure
- `user_portal.html`: Main landing page with three action buttons
- `vote_page.html`: Voting form with radio buttons for each category
- `feedback_page.html`: Feedback form with text areas and satisfaction rating

## Dependencies
Key Python packages: pandas, google-cloud-firestore, google-cloud-storage, python-dotenv, qrcode, Pillow, Flask, gunicorn, sendgrid