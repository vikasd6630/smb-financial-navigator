from google.cloud import firestore
from app.utils.config import settings


class FirestoreClient:
    def __init__(self):
        self.client = firestore.Client(project="settings.GCP_PROJECT_ID")

    def save_funding_query(self, data: dict):
        doc_ref = self.client.collection("funding_queries").document()
        doc_ref.set(data)
        return doc_ref.id