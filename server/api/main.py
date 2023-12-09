from fastapi import FastAPI
from pydantic import BaseModel
from auth.server_authentication import elastic_authen
from utils import check_existing_file_name, delete_existing_file
from scraping_execution import scraping_and_data_storing
from sentimental_analysis import sentimental_analysis

import json

app = FastAPI()

index_config = "configuration"

class RequestConfigure(BaseModel):
    base_url: str
    url: str

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.get("/status/db")
def check_status():
    authen = elastic_authen()
    print("authentication: ", authen.info())
    return {"message": authen.info()}


@app.get("/config")
def get_config():
    authen = elastic_authen()
    response = authen.get(index=index_config, id=1)
    return {"message": response["_source"]}


@app.post("/config")
def create_config(config: RequestConfigure):
    authen = elastic_authen()
    response = authen.index(index=index_config, id=1, body=config.dict())
    return {"message": response["result"]}


# file management
@app.get("/check-files")
def check_existing_file():
    file_name = check_existing_file_name()
    return {"message": file_name}


@app.post("/delete-files/{file_name}")
def delete_file(file_name:str):
    result = delete_existing_file(file_name)
    return {"message": result}


# scraping data and insert to database
@app.post("/scraping-execution")
def scraping_execution():
    result = scraping_and_data_storing()
    return {"message": result}


# sentimental analysis
@app.post("/sentimental-execution")
def sentimental_execution():
    sentimental_analysis()
    return {"message": "sentimental_execution"}
