import requests
import os

# Get the API key from the environment
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

def sign_up(email, password):
    """
    Registers a new user with Firebase Auth.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

def sign_in(email, password):
    """
    Signs in an existing user using Firebase Auth.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

def verify_token(id_token):
    """
    Verifies an ID token with Firebase Auth.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    response = requests.post(url, json={"idToken": id_token})
    return response.json()


