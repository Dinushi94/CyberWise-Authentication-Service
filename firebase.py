import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("firebase-admin-sdk.json")
firebase_admin.initialize_app(cred)