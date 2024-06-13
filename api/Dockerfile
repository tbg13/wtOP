# api/Dockerfile
FROM python:3.11-slim-buster

# Install necessary packages
RUN apt-get update && apt-get install -y \
    vim bash wget openjdk-11-jre-headless build-essential libpq-dev git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && pip install \
    bs4 beautifulsoup4 requests html5lib fastapi uvicorn[standard]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
