import os, json

folder_files = './files'

def check_existing_file_name():
    files = sorted(os.listdir(folder_files), reverse=True)
    return files


def delete_existing_file(file_name):
    if file_name in check_existing_file_name():
        os.remove(folder_files + "/" + file_name)
        return "SUCCESS"
    else:
        print("file not exist")
        return "ERROR"


def total_records(file_name):
    f = open(f'./files/{file_name}', encoding="utf-8")
    total_records = len(json.load(f))
    f.close()
    return total_records

##=== Save sentimental dataset to csv and ElasticSearch
def write_sentimential_dataset(df):
    from auth.server_authentication import elastic_insert_document
    sentimental = "sentimental_dataset"
    df.to_csv(f'./files/{sentimental}.csv', encoding='utf-8', index=False)
    elastic_insert_document(sentimental)

#####====== Convert plots picture into base64 and insert into ElasticSearch
def save_pdf_to_elasticsearch():
    import base64
    from auth.server_authentication import elastic_authen
    file_path = './files/plots.pdf'
    # Read the PDF file and encode it into base64
    with open(file_path, 'rb') as f:
        encoded_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Create the document to be indexed
    doc = {
        'file': encoded_pdf,
        'path': file_path,
    }

    # Index the document
    res = elastic_authen().index(index="sentimental_plots", id=1, body=doc)

    return res

def pdf_sentimental_plot():
    from fastapi.responses import FileResponse
    from pathlib import Path
    # Provide the path to your PDF file
    pdf_path = Path("./files/plots.pdf")

    # Check if the file exists
    if pdf_path.is_file():
        # Return the PDF file using FileResponse
        return FileResponse(pdf_path, media_type="application/pdf", filename="sentimental_plots.pdf")
    else:
        # If the file doesn't exist, return an HTTP 404 response
        return {"error": "File not found"}, 404