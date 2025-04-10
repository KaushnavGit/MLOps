import os
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred_path = os.getenv("FIREBASE_CRED_PATH")  # Add to .env
cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    app = initialize_app(cred, {
        'projectId': cred.project_id  # Explicitly specify project ID from the credential
    })  # initialize the app if it hasn't been initialized already
else:
    app = firebase_admin.get_app()

db = firestore.client()
