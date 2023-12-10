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

def elastic_select_dataset(index_name):
    from fastapi import HTTPException
    record_size = 1000 if index_name == "domains_cleaned" else 30000
    try:
        client_conn = elastic_authen()
        # Perform a search query to retrieve data from Elasticsearch
        response = client_conn.search(index=index_name, body={"query": {"match_all": {}}, "track_total_hits": True}, size=record_size)

        # Extract relevant information from the response
        hits = response['hits']['hits']
        data = [{"_id": hit['_id'], **hit['_source']} for hit in hits]

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data from Elasticsearch: {str(e)}")