from google.cloud import firestore

from .debugging import app_logger as log
from .models import ProcessedPost

def persist_no_op(*args, **kwargs):
    pass

def get_database_client() -> firestore.Client:
    return firestore.Client()

def persist(client, pubname, collname, doc_id, document_dict):
    pass

def increment_publication(client, pubname, count):
    pass