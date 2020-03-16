"""
Here we'll prepare the documents (dicts) to be inserted
in the mongodb.
"""
from webapp.mongo import dao


def insert_many_documents(document_list, collection_name):
    dao.insert_many_documents(document_list, collection_name)
