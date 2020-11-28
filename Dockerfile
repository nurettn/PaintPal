FROM python:3.9-alpine
MAINTAINER Nurettin ABACI

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add bash build-base python3-dev libffi-dev openssl-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user