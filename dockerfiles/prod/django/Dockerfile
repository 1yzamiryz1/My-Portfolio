# pull official base image
FROM python:3.10-slim-buster

LABEL maintainer="1yzamiryz1@gmail.com"

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY ./requirements.txt .
RUN pip install --default-timeout=100 --upgrade pip && pip install -r requirements.txt

# copy project
COPY ./core .
