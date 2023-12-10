from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from typing_extensions import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from auth.server_authentication import elastic_authen
from utils import check_existing_file_name, delete_existing_file
from scraping_execution import scraping_and_data_storing
from sentimental_analysis import sentimental_analysis
from dotenv import load_dotenv   #for python-dotenv method
import os
load_dotenv()

index_config = "configuration"

# openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

sample_user = {
    "supplychain": {
        "username": "supplychain",
        "full_name": "Supply Chain",
        "email": "savanbandith@gmail.com",
        "hashed_password": "$2b$12$yw8S1ijKMwL2vEb.IiT3oeDbPXcxuOn20N4eA3.EFMTBVzsHFc5cK",
        "disabled": False,
    }
}

class RequestConfigure(BaseModel):
    base_url: str
    url: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class CreateUser(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    disabled: bool


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="FastAPI Supply Chain Project",
    description="Supply Chain for Final Project at DST",
    version="1.0.0",
    openapi_tags=[
        {"name": "TEST", "description": "Testing with github action."},
        {"name": "DATASET", "description": "API for checking the existing dataset store in CSV and JSON file."},
        {"name": "EXECUTION", "description": "API for execution scraping, data cleaning, sentimental and etc."},
        {"name": "SECURITY", "description": "API for generate token and get user detail."},
    ],
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(sample_user, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Generate jwt for authentication on protected route
@app.post("/token", response_model=Token, tags=["SECURITY"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(sample_user, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Protected route for get user detail
@app.get("/users/me/", response_model=User, tags=["SECURITY"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


# un-protected route for test cdci
@app.get("/test", tags=["TEST"])
def test_api():
    return {"message": "SUCCESS Testing API for Supply chain project"}


# Un-protected route for check db status
@app.get("/status/db", tags=["TEST"])
def check_db_status(current_user: Annotated[User, Depends(get_current_active_user)]):
    authen = elastic_authen()
    print("authentication: ", authen.info())
    return {"message": authen.info()}


# @app.get("/config")
# def get_config():
#     authen = elastic_authen()
#     response = authen.get(index=index_config, id=1)
#     return {"message": response["_source"]}


# @app.post("/config")
# def create_config(config: RequestConfigure):
#     authen = elastic_authen()
#     response = authen.index(index=index_config, id=1, body=config.dict())
#     return {"message": response["result"]}


# Un-protected route for checking the existing dataset CSV and JSON
@app.get("/check-files", tags=["DATASET"])
def check_existing_file():
    file_name = check_existing_file_name()
    return {"message": file_name}


# Protected route for deleting the existing dataset CSV and JSON
@app.post("/delete-files/{file_name}", tags=["DATASET"])
def delete_file(file_name:str, current_user: Annotated[User, Depends(get_current_active_user)]):
    result = delete_existing_file(file_name)
    return {"message": result}


# Protected route for scraping data and insert to database
@app.post("/scraping-execution", tags=["EXECUTION"])
def scraping_execution(current_user: Annotated[User, Depends(get_current_active_user)]):
    result = scraping_and_data_storing()
    return {"message": result}


# Protected route for sentimental analysis
@app.post("/sentimental-execution", tags=["EXECUTION"])
def sentimental_execution(current_user: Annotated[User, Depends(get_current_active_user)]):
    # output = sentimental_analysis()
    return sentimental_analysis()


# Un-protected route for download sentimental plot
@app.get("/sentimental-plot", tags=["EXECUTION"])
def sentimental_plot():
    from utils import pdf_sentimental_plot
    return pdf_sentimental_plot()