# System Monitoring Dashboard

**System Monitoring Dashboard** is a Flask-based web application that displays real-time system metrics, CPU, memory, and disk usage and stores the latest five metrics in Redis. It’s designed to be easily deployed locally or via Docker, and it integrates with several advanced Docker productivity tools.

## Features

- **Real-time Metrics:** Monitor CPU, memory, and disk usage.
- **Data Persistence:** Save the latest five metrics in Redis.
- **Live Dashboard:** Automatically update the dashboard every 5 seconds.
- **Containerized Deployment:** Easily deploy using Docker and Docker Compose.

## Getting Started

### Prerequisites

- **Local Development:**
  - Python 3.9 or higher
  - Redis installed and running locally ([Installation instructions](https://redis.io/download))
- **Containerized Deployment:**
  - [Docker](https://www.docker.com/get-started)
  - [Docker Compose](https://docs.docker.com/compose/install/)

## Running Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/chintanboghara/system-monitoring-dashboard.git
   cd system-monitoring-dashboard
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Redis is running locally.**

5. **Run the Flask application:**

   ```bash
   flask run --host=0.0.0.0 --port=5001
   ```
   Alternatively:
   ```bash
   python app.py
   ```

6. **Access the application:**

   Open your browser and navigate to [http://localhost:5001](http://localhost:5001).

## Running Using Docker

### Using Dockerfile

1. **Build the Docker image:**

   ```bash
   docker build -t system-monitoring-dashboard .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 5001:5001 system-monitoring-dashboard
   ```

3. **Access the application:**

   Open your browser and navigate to [http://localhost:5001](http://localhost:5001).

### Using Docker Compose

1. **Ensure Docker Compose is installed.**

2. **Start the services:**

   ```bash
   docker-compose up
   ```

   This command builds and starts both the Flask web service and the Redis service.

3. **Access the application:**

   Open your browser and navigate to [http://localhost:5001](http://localhost:5001).

## Advanced Docker Productivity Tools

### Docker Desktop

- **Overview:**  
  Docker Desktop provides a GUI for managing containers, images, and networks. It is highly useful for monitoring container status, logs, and performance metrics.
- **Steps:**  
  - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) on your machine.
  - Launch Docker Desktop to manage your containers and view real-time logs of your running services.

### Docker Build Cloud

- **Overview:**  
  Use Docker Build Cloud (via Buildx) to speed up your build process with advanced caching and parallel builds.
- **Steps:**  
  ```bash
  docker buildx version
  docker buildx create --name mybuilder --use
  docker buildx bake --progress=plain
  ```
  This set of commands helps you create a new builder instance and optimize your build process.

### Docker Scout

- **Overview:**  
  Docker Scout helps you scan your Docker images for security vulnerabilities and outdated dependencies.
- **Steps:**  
  ```bash
  docker scout quickview system-monitoring-dashboard
  docker scout cves system-monitoring-dashboard
  ```
  These commands provide a quick security overview and list of known vulnerabilities for your image.

### Docker Hub

- **Overview:**  
  Docker Hub is a central repository for sharing your Docker images.
- **Steps to Push Your Image:**
  1. **Log in to Docker Hub:**
     ```bash
     docker login --username YOUR_DOCKERHUB_USERNAME
     ```
  2. **Build your image (if not already built):**
     ```bash
     docker build -t YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard .
     ```
  3. **Push the image to Docker Hub:**
     ```bash
     docker push YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest
     ```

### Test with Testcontainers Cloud

- **Overview:**  
  Testcontainers Cloud allows you to run integration tests in isolated container environments. It is ideal for ensuring your application works as expected when interfacing with external services like Redis.
- **Steps:**
  - **Install Dependencies:**
    ```bash
    pip install pytest testcontainers
    ```
  - **Example Test File:**  
    Create a file named `test_app.py` with the following content:
    ```python
    import pytest
    import redis
    import os
    from testcontainers.redis import RedisContainer
    from app import app

    @pytest.fixture(scope="module")
    def redis_container():
        with RedisContainer() as redis_container:
            redis_host = redis_container.get_container_host_ip()
            redis_port = redis_container.get_exposed_port(6379)
            os.environ["REDIS_HOST"] = redis_host
            os.environ["REDIS_PORT"] = str(redis_port)
            yield redis_host, redis_port

    @pytest.fixture
    def client():
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_redis_connection(redis_container):
        redis_host, redis_port = redis_container
        r = redis.Redis(host=redis_host, port=int(redis_port), decode_responses=True)
        r.set("test_key", "Hello, Redis!")
        assert r.get("test_key") == "Hello, Redis!"

    def test_metrics_endpoint(client):
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.get_json()
        assert "cpu" in data
        assert "memory" in data
        assert "disk" in data
    ```
  - **Run the Tests:**
    ```bash
    python3 -m pytest test_app.py
    ```

## Summary of Key Commands

| Feature             | Command                                             |
|---------------------|-----------------------------------------------------|
| **Build Image**     | `docker build -t system-monitoring-dashboard .`     |
| **Run Container**   | `docker run -p 5001:5001 system-monitoring-dashboard` |
| **Start Services**  | `docker-compose up`                                 |
| **Stop Services**   | `docker-compose down`                               |
| **Live Reload**     | `docker-compose watch`                              |
| **Security Scan**   | `docker scout quickview system-monitoring-dashboard`|
| **Faster Build**    | `docker buildx bake --progress=plain`               |
| **Push to Docker Hub** | See steps under **Docker Hub**                  |
| **Run Tests**       | `pytest test_app.py`                                |
