FROM python:3.10-alpine

RUN apk update 
RUN apk add python3-dev cmake gfortran gcc libc-dev g++

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip freeze

COPY . .
ENTRYPOINT [ "python", "main.py" ]
