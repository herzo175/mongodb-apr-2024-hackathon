FROM python:3.10-slim-bookworm

RUN apt update
RUN apt install -y python3-dev cmake gfortran gcc libc-dev g++
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash apt-get install git-lfs
RUN git lfs install

WORKDIR /models
RUN git clone https://huggingface.co/openai/clip-vit-base-patch32

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "python", "main.py" ]
