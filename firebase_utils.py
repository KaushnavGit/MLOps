import json
from datetime import datetime, timedelta
from config import db

def normalize_email(email: str) -> str:
    """Normalize the email to use as Firestore document ID by replacing '.' with '_'."""
    return email.replace(".", "_")

def save_submission(email, data):
    """
    Save a submission under the user's document in the 'users' collection.
    Submissions are saved in the 'submissions' subcollection.
    """
    user_id = normalize_email(email)
    user_doc_ref = db.collection("users").document(user_id)
    # Create or merge the user document with the email field.
    user_doc_ref.set({"email": email}, merge=True)
    # Save the submission document.
    return user_doc_ref.collection("submissions").add(data)

def has_valid_submission(email):
    """
    Checks if the user has any submission made within the last 90 days.
    """
    user_id = normalize_email(email)
    subs_ref = db.collection("users").document(user_id).collection("submissions")
    submissions = subs_ref.stream()
    
    for sub in submissions:
        sub_data = sub.to_dict()
        if "submitted_at" in sub_data:
            try:
                submitted_time = datetime.fromisoformat(sub_data["submitted_at"])
                if datetime.utcnow() - submitted_time < timedelta(days=90):
                    return True
            except Exception:
                continue
    return False

def get_all_submissions():
    """
    Fetch all submissions from all users by iterating over the 'users' collection.
    Alternatively, a collection group query could be used.
    """
    all_submissions = []
    users_ref = db.collection("users").stream()
    for user in users_ref:
        submissions_ref = db.collection("users").document(user.id).collection("submissions").stream()
        for sub in submissions_ref:
            sub_data = sub.to_dict()
            # Include the user's email in the data for display purposes.
            sub_data["email"] = user.to_dict().get("email", "N/A")
            all_submissions.append(sub_data)
    return all_submissions

def is_manually_approved(email):
    """
    Check if the user is manually approved by reading the corresponding document 
    in the 'manual_access' collection.
    """
    user_id = normalize_email(email)
    doc = db.collection("manual_access").document(user_id).get()
    return doc.exists and doc.to_dict().get("approved", False)

def request_access(email):
    """
    Record an access request in the 'access_requests' collection.
    """
    user_id = normalize_email(email)
    db.collection("access_requests").document(user_id).set({
        "email": email,
        "requested_at": datetime.utcnow().isoformat()
    })
