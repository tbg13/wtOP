# Docker setup for main
FROM alpine:latest

# Install necessary packages
RUN apk update && apk add --no-cache \
    vim bash python3 py3-pip wget openjdk11-jre-headless build-base libpq-dev git && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Create and activate a venv to install Python libraries
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && pip install \
    dagster dagit \
    dbt-core dbt-duckdb duckdb

# Install MinIO server and client
RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio && \
    wget https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x minio mc && mv minio /usr/local/bin/ && mv mc /usr/local/bin/

EXPOSE 3000 9000

CMD ["sh", "-c", "minio server /app/minio & tail -f /dev/null"]
