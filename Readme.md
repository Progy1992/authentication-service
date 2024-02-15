# Running Flask App Using Docker Build and Gunicorn

## Steps

### 1. Build the Docker Image

In the terminal, navigate to your project directory and build the Docker image:

```bash
docker build -t auth_service .
```

### 2. Run the Docker Container

Once the image is built, you can run the Docker container:

```bash
docker run -d -p 8000:8000 auth_service
```

Your Flask app will be accessible at `http://localhost:8000`.