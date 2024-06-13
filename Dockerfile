# Docker setup for dev environment
FROM alpine:latest

# Install packages
RUN apk update && apk add --no-cache \
vim \
bash \
python3 \
py3-pip \
wget \
openjdk11-jre \
build-base \
libpq-dev

WORKDIR /app

# Create and activate a venv to install Python libraries
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install \
bs4 beautifulsoup4 requests html5lib \
fastapi uvicorn[standard] \
octavia-cli \
dbt-core dbt-duckdb duckdb

# Install MinIO server and client
RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio && \
    wget https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x minio mc && \
    mv minio /usr/local/bin/ && \
    mv mc /usr/local/bin/

# Install Airbyte CLI (latest stable version v0.63.0)
ENV AIRBYTE_CLI_VERSION 0.63.0
RUN wget https://github.com/airbytehq/airbyte/releases/download/v${AIRBYTE_CLI_VERSION}/airbyte-cli-${AIRBYTE_CLI_VERSION}.tar.gz && \
    tar -xzf airbyte-cli-${AIRBYTE_CLI_VERSION}.tar.gz && \
    mv airbyte /usr/local/bin/ && \
    rm airbyte-cli-${AIRBYTE_CLI_VERSION}.tar.gz

EXPOSE 3000 8000 9000

CMD ["sh", "-c", "minio server /app/minio & tail -f /dev/null"]
