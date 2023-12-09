import os
from file_handling import open_json_domain_file, open_json_comment_file
from cleaning_data import cleaning_domains, cleaning_comments
from auth.server_authentication import elastic_insert_document
from scraping_functions import main_scraping, check_reviewer_in_each_domain


url = "https://www.trustpilot.com/categories/financial_institution"
json_domain_file = "domains.json"
json_comment_file = "comments.json"

def scraping_and_data_storing():
    raw_data_domains = open_json_domain_file(json_domain_file) if os.path.isfile(f"./files/{json_domain_file}") else main_scraping(url)
    raw_data_comments = open_json_comment_file(json_comment_file) if os.path.isfile(f"./files/{json_comment_file}") else check_reviewer_in_each_domain(raw_data_domains)

    elastic_insert_document("domains") ### Execution elastic
    elastic_insert_document("comments") ### Execution elastic

    cleaning_domains() ### Domains Data Cleaning
    cleaning_comments() ### Comments Data Cleaning

    return {"message": "SUCCESS"}

