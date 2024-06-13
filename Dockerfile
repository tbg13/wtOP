# Docker setup for dev environment
FROM alpine:latest

# Install necessary packages
RUN apk update && apk add --no-cache \
    vim \
    bash \
    python3 \
    py3-pip \
    wget \
    openjdk11-jre \
    build-base \
    libpq-dev \
    git \

WORKDIR /app

# Create and activate a venv to install Python libraries
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel

RUN pip install bs4 beautifulsoup4 requests html5lib
RUN pip install fastapi uvicorn[standard]
RUN pip install dbt-core dbt-duckdb duckdb

# Install MinIO server and client
RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio && \
    wget https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x minio mc && \
    mv minio /usr/local/bin/ && \
    mv mc /usr/local/bin/

EXPOSE 3000 8000 9000

CMD ["sh", "-c", "minio server /app/minio & tail -f /dev/null"]
