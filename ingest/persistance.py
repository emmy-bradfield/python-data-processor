from google.cloud import firestore

from .debugging import app_logger as log
from .models import ProcessedPost

def persist_no_op(*args, **kwargs):
    pass

def get_database_client() -> firestore.Client:
    return firestore.Client()

def persist(client, pubname, collname, doc_id, document_dict):
    if collname is None or doc_id is None:
        increment_publication(client, pubname, document_dict['count'])
    else: 
        document_dict['count'] = firestore.Increment(document_dict['count'])
        pubdoc = client.collection(u'publications').document(pubname)
        wrddoc = pubdoc.collection(collname).document(doc_id)
        wrddoc.set(document_dict, merge=True)
        log.debug('incremented word counter')

def increment_publication(client, pubname, count):
    pubdoc = client.collection(u'publications').document(pubname)
    pubdoc.set({'count': firestore.Increment(count)}, merge=True)
    log.debug(f'incremented publication counter for {pubname}')