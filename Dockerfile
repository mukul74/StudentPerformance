FROM python:3.8-slim-buster
WORKDIR /stapp
COPY . /stapp
RUN apt update -y && apt install awscli -y
RUN pip install -r requirements.txt 
CMD python3 application.py
