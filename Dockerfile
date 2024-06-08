# Docker setup for dev environment
FROM alpine:latest

# Install packages
RUN apk update && apk add --no-cache \
vim \
bash \
python3 \
py3-pip

WORKDIR /app

# Create and activate a venv to install Python libraries
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install \
fastapi \
bs4 beautifulsoup4 requests html5lib

EXPOSE 3000 8000

CMD ["bash"]