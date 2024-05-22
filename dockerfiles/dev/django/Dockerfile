FROM python:3.10-slim-buster

LABEL maintainer="1yzamiryz1@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip install debugpy

COPY ./core /app