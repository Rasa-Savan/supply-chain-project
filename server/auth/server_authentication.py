import os 
from elasticsearch import Elasticsearch
from file_handling import import_csv_to_elastic
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()

def elastic_authen():
    client = Elasticsearch(
        "https://es01:9200",
        ca_certs="/etc/ssl/certs/http_ca.crt",
        basic_auth=(os.environ.get('ES_USERNAME'), os.environ.get('ES_PASSWORD'))
    )

    if client.info(): print("\n\nElasticSearch is 'CONNECTED'")
    return client


def elastic_insert_document(index_name):
    client_conn = elastic_authen()
    print("Please wait while system is inserting data to ElasticSearch...")

    has_index = client_conn.indices.exists(index=index_name)
    if not has_index: client_conn.indices.create(index=index_name)

    is_doc_delete = True
    if is_doc_delete:
        print("Deleting existing document...")
        client_conn.delete_by_query(index=index_name, query={"match_all": {}})
        print("Deleting existing document... >>> DONE")
    
    import_csv_to_elastic(client_conn, index_name)