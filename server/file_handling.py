# from util.constants import constants
from elasticsearch import helpers
import json, csv, pandas

csv_domain_file = "domains.csv"
csv_comment_file = "comments.csv"
csv_domain_cleaned_file = "domains_cleaned.csv"
csv_comment_cleaned_file = "comments_cleaned.csv"
csv_sentimental_textblob_file = "sentimental_dataset.csv"
json_domain_file = "domains.json"
json_comment_file = "comments.json"


def open_json_domain_file(r_domain_file):
    # Opening JSON file
    f = open(f'./files/{r_domain_file}', encoding="utf8")
    raw_data_domains = json.load(f)
    f.close()
    
    write_domain_to_csv(raw_data_domains)
    return raw_data_domains

def open_json_comment_file(r_comment_file):
    # Opening JSON file
    f = open(f'./files/{r_comment_file}', encoding="utf8")
    raw_data_comment = json.load(f)
    f.close()
    
    write_comments_to_csv(raw_data_comment)
    return raw_data_comment


def write_domain_to_csv(r_raw_data_domains):
    print("\n\nCSV domains data is writing, please wait...")
    df = pandas.DataFrame(r_raw_data_domains)
    df.to_csv(f'./files/{csv_domain_file}', encoding='utf-8', index=False)
    print("CSV domains file is 'COMPLETED'")


def write_comments_to_csv(r_list_all_comments):
    print("\n\nCSV comments data is writing, please wait...")
    df = pandas.DataFrame(r_list_all_comments)
    df.to_csv(f'./files/{csv_comment_file}', encoding='utf-8', index=False)
    print("CSV comments file is 'COMPLETED'")


def write_domain_to_json(r_raw_data_domains):
    print("\n\nJSON data is writing, please wait...")
    with open(f'./files/{json_domain_file}', 'w', encoding="utf-8") as f:
        json.dump(r_raw_data_domains , f, indent=2, ensure_ascii=False)
    print("JSON domains file is 'COMPLETED'")
    open_json_domain_file(json_domain_file)


def write_comments_to_json(r_list_all_comments):
    print("\n\nJSON comments data is writing, please wait...")
    with open(f'./files/{json_comment_file}', 'w', encoding='utf-8') as f:
        json.dump(r_list_all_comments , f, indent=2, ensure_ascii=False)
    print("JSON domains file is 'COMPLETED'")


def import_csv_to_elastic(r_client_conn, r_index_name):
    # file_name = constants["csv_domain_file"] if r_index_name == constants["domain_table_name"] else constants["csv_comment_file"]
    file_name = ""
    if r_index_name == "domains": file_name = csv_domain_file
    if r_index_name == "comments": file_name = csv_comment_file
    if r_index_name == "domains_cleaned": file_name = csv_domain_cleaned_file
    if r_index_name == "comments_cleaned": file_name = csv_comment_cleaned_file
    if r_index_name == "sentimental_dataset": file_name = csv_sentimental_textblob_file

    with open(f'./files/{file_name}', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        # for row in csv_reader:
        #     r_client_conn.index(index=r_index_name, document=dict(row))
        helpers.bulk(r_client_conn, csv_reader, index=r_index_name)

    print(f"Inserted {r_index_name} to ElasticSearch is 'COMPLETED'")


# def read_domains_json_file():
#     f = open(f'./files/{constants["json_domain_file"]}', encoding="utf8")
#     raw_data_domains = json.load(f)
#     f.close()
#     return raw_data_domains