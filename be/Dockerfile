FROM python:3.12-rc-slim-bullseye AS builder

RUN apt-get update && apt-get install -y unzip git libmecab-dev mecab && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ADD https://clrd.ninjal.ac.jp/unidic_archive/2302/unidic-csj-202302.zip unidic.zip
RUN unzip unidic.zip -d dicdir && rm -f unidic.zip
ENV DICDIR "/app/dicdir"
RUN python3 -m pip install --no-cache-dir -U pip
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
