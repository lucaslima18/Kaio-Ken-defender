FROM python:3.13-slim

# Install system dependencies and Nuclei
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://github.com/projectdiscovery/nuclei/releases/download/v3.4.10/nuclei_3.4.10_linux_amd64.zip \
    && unzip nuclei_3.4.10_linux_amd64.zip \
    && mv nuclei /usr/local/bin/ \
    && chmod +x /usr/local/bin/nuclei \
    && rm nuclei_3.4.10_linux_amd64.zip LICENSE.md README.md \
    && pip install --upgrade pip && pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root \
    && nuclei -update-templates \
    && mkdir -p /app/data

COPY . .