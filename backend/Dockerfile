FROM python:3.10-slim-bookworm

RUN apt update
RUN apt install -y python3-dev cmake gfortran gcc libc-dev g++

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "python", "main.py" ]
