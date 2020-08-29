FROM python:3.8-slim-buster

MAINTAINER Nurettin ABACI

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get -y install --no-install-recommends \
    binutils \
    && rm -rf /var/lib/apt/lists/*


#RUN apk add --no-cache jpeg-dev zlib-dev
#RUN apk add --no-cache --virtual .builds-deps \
#    build-base linux-headers


COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /requirements.txt




RUN mkdir /app
WORKDIR /app
COPY ./app /app

# COPY . /app
# pip install /app/requirements.txt

RUN groupadd -r django && useradd -r -g django django
USER django
