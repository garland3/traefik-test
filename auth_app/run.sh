docker build -t auth .
# get .env from parent directory
docker run -p 5000:5000 -v $(pwd)/../.env:/app/.env -t auth