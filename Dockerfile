FROM python:3.8-slim

COPY src/requirements.txt ./

RUN apt-get update \
    && apt-get --no-install-recommends -y install \
      build-essential \
      python-psycopg2 \
      libpq-dev \
      python-dev \
      libcairo2 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libgdk-pixbuf2.0-0 \
      libffi-dev \
      shared-mime-info \
      libmagic1 \
    && apt-mark manual \
      libpq5 \
      python \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install uwsgi \
    && apt-get remove -y \
      libpq-dev \
      python-dev \
      build-essential \
    && apt-get -y autoclean && apt-get -y autoremove && apt-get -y clean

ADD src /srv

WORKDIR /srv