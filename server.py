import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string, render_template, redirect, url_for
from google.cloud import firestore

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
COLLECTION_NAME = os.getenv("COLLECTION_NAME") # Main guest collection
VOTES_COLLECTION_NAME = "Startup-World-Cup-Seattle-Regional-Votes" # New collection for votes
FEEDBACK_COLLECTION_NAME = "Startup-World-Cup-Seattle-Regional-Feedback" # New collection for feedback

app = Flask(__name__)

COMPANIES = [
    "Airbuild",
    "Cromodata",
    "Eco SmarTiles",
    "Emerald Battery Labs",
    "GreenThumb AI",
    "Koidra",
    "Pivotal Build",
    "RealEngineers",
    "REearthable",
    "Zesty"
]

@app.route("/checkin", methods=["GET"])
def checkin():
    email = request.args.get("email")
    if not email:
        return "Missing email parameter.", 400
    try:
        db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
        collection_ref = db.collection(COLLECTION_NAME)
        query = collection_ref.where("email", "==", email).limit(1)
        docs = list(query.stream())
        if not docs:
            return f"No document found for email: {email}", 404
        doc_ref = docs[0].reference
        doc_ref.update({"check_in": 1})
        # Redirect to the user portal with a success message
        return redirect(url_for("user_portal", email=email, checkin_successful=True))
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route("/user_portal")
def user_portal():
    email = request.args.get("email")
    checkin_successful_param = request.args.get("checkin_successful") == "True"
    vote_successful_param = request.args.get("vote_successful") == "True"
    feedback_successful_param = request.args.get("feedback_successful") == "True"

    if not email:
        return "Missing email parameter.", 400

    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    collection_ref = db.collection(COLLECTION_NAME)
    votes_collection_ref = db.collection(VOTES_COLLECTION_NAME)
    feedback_collection_ref = db.collection(FEEDBACK_COLLECTION_NAME)

    status_message = None
    is_checkin_disabled = False
    is_vote_disabled = False
    is_feedback_disabled = False

    # Fetch Firestore data for current user
    user_doc_query = collection_ref.where("email", "==", email).limit(1)
    user_docs = list(user_doc_query.stream())
    user_data = user_docs[0].to_dict() if user_docs else {}

    user_vote_doc = votes_collection_ref.document(email).get()
    user_feedback_doc = feedback_collection_ref.document(email).get()

    # Determine button disabled states based on Firestore data
    if user_data.get("check_in") == 1:
        is_checkin_disabled = True
    
    if user_vote_doc.exists:
        is_vote_disabled = True

    if user_feedback_doc.exists:
        is_feedback_disabled = True

    # Determine status message based on explicit success parameters or existing Firestore data
    if checkin_successful_param:
        status_message = "Thank you for checking in! We're glad to have you with us—let's make today amazing.\nDon't forget to vote for your favorite startup and share your feedback about this event to help us make future experiences even better."
    elif vote_successful_param:
        status_message = "Thank you for your vote! Your voice helps shape the future of these startups."
    elif feedback_successful_param:
        status_message = "Thank you for your feedback! We appreciate you taking the time to help us improve future events."
    elif is_checkin_disabled and is_vote_disabled and is_feedback_disabled:
        status_message = "All actions completed! Thank you for your participation."
    elif is_checkin_disabled and is_vote_disabled:
        status_message = "You have already checked in and voted! Please consider providing event feedback."
    elif is_checkin_disabled and is_feedback_disabled:
        status_message = "You have already checked in and provided feedback! Please consider voting for startups."
    elif is_vote_disabled and is_feedback_disabled:
        status_message = "You have already voted and provided feedback!"
    elif is_checkin_disabled:
        status_message = "You have already checked in! Don't forget to vote for your favorite startup and share your feedback."
    elif is_vote_disabled:
        status_message = "You have already submitted your votes! Please check in and share your feedback."
    elif is_feedback_disabled:
        status_message = "You have already submitted your feedback! Please check in and vote for startups."

    checkin_url = f"/checkin?email={email}"
    vote_url = f"/vote?email={email}"
    feedback_url = f"/feedback?email={email}"

    return render_template(
        "user_portal.html",
        checkin_url=checkin_url,
        vote_url=vote_url,
        feedback_url=feedback_url,
        status_message=status_message,
        is_checkin_disabled=is_checkin_disabled,
        is_vote_disabled=is_vote_disabled,
        is_feedback_disabled=is_feedback_disabled
    )

@app.route("/vote", methods=["GET"])
def vote_page():
    email = request.args.get("email")
    vote_submitted = request.args.get("vote_submitted", False)

    if not email:
        return "Missing email parameter.", 400

    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    votes_collection_ref = db.collection(VOTES_COLLECTION_NAME)
    
    is_vote_disabled = False
    vote_status_message = None

    # Check if the user has already voted
    user_vote_doc = votes_collection_ref.document(email).get()
    if user_vote_doc.exists:
        is_vote_disabled = True
        vote_status_message = "Thank you for your vote! Your voice helps shape the future of these startups. You have already submitted your votes."
    elif vote_submitted:
        is_vote_disabled = True # Disable if just submitted
        vote_status_message = "Thank you for your vote! Your voice helps shape the future of these startups."

    return render_template(
        "vote_page.html",
        email=email,
        companies=COMPANIES,
        is_vote_disabled=is_vote_disabled,
        vote_status_message=vote_status_message
    )

@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    email = request.form.get("email")
    inspiring_pitch = request.form.get("inspiring_pitch")
    crowd_favorite = request.form.get("crowd_favorite")
    innovative_idea = request.form.get("innovative_idea")

    if not email:
        return "Missing email in form submission.", 400

    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    votes_collection_ref = db.collection(VOTES_COLLECTION_NAME)

    # Prevent duplicate submissions
    user_vote_doc = votes_collection_ref.document(email).get()
    if user_vote_doc.exists:
        # Redirect back to vote page with message that they already voted
        return redirect(url_for("vote_page", email=email, vote_submitted=False))

    vote_data = {
        "email": email,
        "inspiring_pitch": inspiring_pitch,
        "crowd_favorite": crowd_favorite,
        "innovative_idea": innovative_idea,
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    try:
        votes_collection_ref.document(email).set(vote_data)
        # Redirect to the user portal with a success message
        return redirect(url_for("user_portal", email=email, vote_successful=True))
    except Exception as e:
        return f"An error occurred while submitting vote: {e}", 500

@app.route("/feedback", methods=["GET"])
def feedback_page():
    email = request.args.get("email")
    feedback_submitted = request.args.get("feedback_submitted", False)

    if not email:
        return "Missing email parameter.", 400

    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    feedback_collection_ref = db.collection(FEEDBACK_COLLECTION_NAME)
    
    is_feedback_disabled = False
    feedback_status_message = None

    # Check if the user has already submitted feedback
    user_feedback_doc = feedback_collection_ref.document(email).get()
    if user_feedback_doc.exists:
        is_feedback_disabled = True
        feedback_status_message = "Thank you for your feedback! We appreciate you taking the time to help us improve future events. You have already submitted your feedback."
    elif feedback_submitted:
        is_feedback_disabled = True # Disable if just submitted
        feedback_status_message = "Thank you for your feedback! We appreciate you taking the time to help us improve future events."

    return render_template(
        "feedback_page.html",
        email=email,
        is_feedback_disabled=is_feedback_disabled,
        feedback_status_message=feedback_status_message
    )

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    email = request.form.get("email")
    overall_satisfaction = request.form.get("overall_satisfaction")
    liked_most = request.form.get("liked_most")
    suggestions = request.form.get("suggestions")

    if not email:
        return "Missing email in form submission.", 400

    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    feedback_collection_ref = db.collection(FEEDBACK_COLLECTION_NAME)

    # Prevent duplicate submissions
    user_feedback_doc = feedback_collection_ref.document(email).get()
    if user_feedback_doc.exists:
        # Redirect back to feedback page with message that they already submitted
        return redirect(url_for("feedback_page", email=email, feedback_submitted=False))

    feedback_data = {
        "email": email,
        "overall_satisfaction": overall_satisfaction,
        "liked_most": liked_most,
        "suggestions": suggestions,
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    try:
        feedback_collection_ref.document(email).set(feedback_data)
        # Redirect to the user portal with a success message
        return redirect(url_for("user_portal", email=email, feedback_successful=True))
    except Exception as e:
        return f"An error occurred while submitting feedback: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001) 