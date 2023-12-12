from auth.server_authentication import elastic_authen, elastic_insert_document
from utils import total_records
import pandas as pd
import json

domain_cleaned_index = "domains_cleaned"
comment_cleaned_index = "comments_cleaned"

def cleaning_domains():
    client = elastic_authen()
    domains_resp = client.search(index="domains", size=total_records("domains.json"))

    domains_raw_data = []
    for hit in domains_resp.body['hits']['hits']:
        domains_raw_data.append(hit["_source"])

    df = pd.DataFrame(domains_raw_data)
    
    df = df[df['reviewers'].notnull()]
    df['reviewers'] = df['reviewers'].apply(lambda x: x.replace(',', '') if ',' in x else x)
    df['reviewers'] = df['reviewers'].apply(lambda x: int(x) if x.strip() else x)
    # df[['State', 'Country']] = df['domain_address'].str.split(', ', n=1, expand=True)
    # df.drop('domain_address', axis=1, inplace=True)

    columns_to_clean = ['star_5', 'star_4', 'star_3', 'star_2', 'star_1']
    for col in columns_to_clean:
        df[col] = df[col].str.replace('%', '', regex=True).str.replace('<', '', regex=True)
        df[col] = df[col].apply(lambda x: int(x) if x.strip() else x)

    df.to_csv(f"files/domains_cleaned.csv", index=False, encoding="utf-8")

    # Write the list of dictionaries to a JSON file
    with open(f"files/domains_cleaned.json", 'w', encoding='utf-8') as json_file:
        json.dump(df.to_dict(orient='records'), json_file, ensure_ascii=False, indent=2)

    elastic_insert_document(domain_cleaned_index)
    # print(df.head(20))

def cleaning_comments():
    client = elastic_authen()
    comments_resp = client.search(index="comments", size=total_records("comments.json"))

    comments_raw_data = []
    for hit in comments_resp.body['hits']['hits']:
        comments_raw_data.append(hit["_source"])

    df = pd.DataFrame(comments_raw_data)

    # Convert 'reviewer_rate' to numeric
    df['reviewer_rate'] = pd.to_numeric(df['reviewer_rate'], errors='coerce')
    
    # Convert 'reviewer_date' to datetime
    df['reviewer_date'] = pd.to_datetime(df['reviewer_date'], errors='coerce')
    df['reviewer_date'] = df['reviewer_date'].dt.strftime('%Y-%m-%d')

    # Text cleansing convert to lower case
    df['reviewer_title'] = df['reviewer_title'].str.lower()
    df['reviewer_message'] = df['reviewer_message'].str.lower()
    df['reply_title'] = df['reply_title'].str.lower()
    df['reply_message'] = df['reply_message'].str.lower()

    # Remove 'Date of experience: ' and Convert 'reviewer_exp_date' to a datetime object, then Convert it to the desired date format 'yyyy-mm-dd'
    df['reviewer_exp_date'] = df['reviewer_exp_date'].str.replace('Date of experience: ', '')
    df['reviewer_exp_date'] = pd.to_datetime(df['reviewer_exp_date'], format='%B %d, %Y', errors='coerce')
    df['reviewer_exp_date'] = df['reviewer_exp_date'].dt.strftime('%Y-%m-%d')

    
    filtered_df = df[df['reviewer_rate'].notnull() & df['reviewer_message'].notnull()]
 
    # Show the resulting DataFrame
    filtered_df.info()

    filtered_df.to_csv(f"files/comments_cleaned.csv", index=False, encoding="utf-8")
    # df.to_csv(f"files/comments_cleaned.csv", index=False, encoding="utf-8")

    # Write the list of dictionaries to a JSON file
    with open(f"files/comments_cleaned.json", 'w', encoding='utf-8') as json_file:
        json.dump(df.to_dict(orient='records'), json_file, ensure_ascii=False, indent=2)

    elastic_insert_document(comment_cleaned_index)
    # print(df.head(20))
    # print(df.shape)