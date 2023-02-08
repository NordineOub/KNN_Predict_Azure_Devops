# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
COPY . . 
RUN pip install -r requirements.txt

# install app
COPY API_flask.py /
COPY knn_Iris.pkl /

# final configuration
ENV FLASK_APP=API_flask
EXPOSE 8000
CMD flask run --host 0.0.0.0 --port 8000