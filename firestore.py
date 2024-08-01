import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate(r"creditial.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def save_to_firestore(data):
    try:
        db.collection("surat_tugas").add(data)
        return True
    except Exception as e:
        print(f"Error saving to Firestore: {e}")
        return False
