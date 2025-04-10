from config import db

def add_entry(email, data_dict):
    """
    Adds a submission under a user’s document in the 'users' collection.
    The submission is stored in the 'submissions' subcollection.
    """
    normalized_email = email.replace(".", "_")
    user_ref = db.collection("users").document(normalized_email)
    # Ensure the user document exists (merge data if necessary)
    user_ref.set({"email": email}, merge=True)
    return user_ref.collection("submissions").add({**data_dict, "email": email})

def fetch_all_entries():
    """
    Fetch all submissions from all users via a collection group query.
    """
    docs = db.collection_group("submissions").stream()
    return [doc.to_dict() for doc in docs]

def fetch_verified_entries():
    """
    Fetch submissions where 'is_verified' is True across all users.
    """
    docs = db.collection_group("submissions").where("is_verified", "==", True).stream()
    return [doc.to_dict() for doc in docs]

def fetch_by_company(company):
    """
    Retrieves submissions filtered by company.
    """
    docs = db.collection_group("submissions").where("company", "==", company).stream()
    return [doc.to_dict() for doc in docs]

def fetch_by_role(role):
    """
    Retrieves submissions filtered by role.
    """
    docs = db.collection_group("submissions").where("role", "==", role).stream()
    return [doc.to_dict() for doc in docs]
