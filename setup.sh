#!/bin/bash

## Build images
docker image build . -t 082503/fastapi-supply-chain:1.0.0 -f Dockerfile

## Push the Docker image to Dockerhub
docker push 082503/fastapi-supply-chain:1.0.0

# ## Run create kubernetes
# kubectl apply -f my-secret-eval.yml
# kubectl apply -f my-deployment-eval.yml
# kubectl apply -f my-service-eval.yml
# kubectl create -f my-ingress-eval.yml

# ## Run docker-compose
# # docker-compose up -d