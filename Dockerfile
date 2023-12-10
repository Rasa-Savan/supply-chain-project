FROM python:3.9

RUN mkdir FastAPI

COPY server/. /FastAPI/server
COPY docker-compose-spc.yml /FastAPI

COPY config/http_ca.crt /etc/ssl/certs
RUN chown root:root /etc/ssl/certs/http_ca.crt

WORKDIR /FastAPI/server

RUN python -m pip install --upgrade pip
RUN pip install "fastapi[all]"

RUN python -m pip install --upgrade pip
RUN pip install "uvicorn[standard]"

RUN python -m pip install --upgrade pip
RUN python -m pip install elasticsearch
RUN python -m pip install "elasticsearch[async]"

RUN python -m pip install --upgrade pip
RUN pip install python-dotenv
RUN pip install pandas
RUN pip install beautifulsoup4
RUN pip install numpy
RUN pip install seaborn

RUN python -m pip install --upgrade pip
RUN python -m pip install -U pip
RUN python -m pip install -U matplotlib
RUN python -m pip install -U nltk

RUN python -m pip install --upgrade pip
RUN python -m pip install -U scikit-learn
RUN python -m pip install textblob
RUN python -m pip install afinn
RUN python -m pip install vaderSentiment


EXPOSE 8008

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8008"]