# Quick launch for local dev
## Build image
docker build -t wtop_image .

## Launch container
docker stop wtop_container
docker remove wtop_container
docker run -d -it -p 3000:3000 -p 8000:8000 -p 9000:9000 -v "$(pwd):/app" -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin --name wtop_container wtop_image

## CD into container
docker exec -it wtop_container /bin/bash

## FastAPI 
### Since using container, need to tell fastapi to listen to all IP addresses from container
fastapi dev main.py --host 0.0.0.0 --port 8000
### Then access from browser at http://127.0.0.1:8000