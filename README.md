# System Monitoring Dashboard

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.x-orange.svg)](https://flask.palletsprojects.com/)
[![Redis](https://img.shields.io/badge/redis-stable-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
<!-- Add other relevant badges like license, build status, etc. -->

**System Monitoring Dashboard** is a lightweight Flask web application designed to display real-time system metrics, including CPU, memory, and disk usage. It leverages Redis to store the five most recent metric readings, providing a historical snapshot. The dashboard automatically refreshes every 5 seconds.

The application is built for easy deployment, either locally for development or containerized using Docker and Docker Compose, integrating seamlessly with advanced Docker productivity tools.

<!-- Consider adding a screenshot or GIF here -->
<!-- ![Dashboard Screenshot](link/to/your/screenshot.png) -->

## Features

-   **Real-time Metrics:** Displays current CPU usage (%), memory usage (%), and disk usage (%).
-   **Data Persistence:** Stores the latest five metric snapshots in a Redis list for historical context.
-   **Live Dashboard:** Frontend automatically fetches and updates metrics every 5 seconds without page reloads.
-   **Containerized:** Ready for deployment using Docker and Docker Compose for consistent environments.
-   **Cross-Platform:** Uses `psutil` to gather system metrics, compatible with Linux, macOS, and Windows.

## Tech Stack

-   **Backend:** Python, Flask
-   **Data Store:** Redis
-   **System Metrics:** `psutil` library
-   **Frontend:** HTML, CSS, JavaScript (Fetch API)
-   **Containerization:** Docker, Docker Compose

## Getting Started

### Prerequisites

Ensure you have the necessary tools installed for your chosen setup method:

-   **Local Development:**
    -   Python 3.9 or higher
    -   `pip` (Python package installer)
    -   Redis Server ([Installation instructions](https://redis.io/download)) running locally (usually on `localhost:6379`).
    -   Git
-   **Containerized Deployment:**
    -   [Docker Engine](https://www.docker.com/get-started)
    -   [Docker Compose](https://docs.docker.com/compose/install/) (v2 recommended)
    -   Git

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chintanboghara/system-monitoring-dashboard.git
    cd system-monitoring-dashboard
    ```

2.  **Set up a virtual environment (Recommended):**
    *Why?* Isolates project dependencies, preventing conflicts with system-wide packages.
    ```bash
    python3 -m venv venv
    # Activate the environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Git Bash/PowerShell):
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note:* `psutil` might require build tools on some systems if a pre-compiled wheel isn't available for your platform/Python version.

4.  **Ensure Redis is running:**
    Verify your local Redis server is active. You can test the connection using `redis-cli ping` (should return `PONG`).

5.  **Run the Flask application:**
    There are two common ways:
    *   Using the `flask` command (recommended for development, enables debug mode):
        ```bash
        # Ensure FLASK_APP=app.py is set (often automatic)
        # Optional: export FLASK_ENV=development for debug mode
        flask run --host=0.0.0.0 --port=5001
        ```
    *   Directly executing the Python script:
        ```bash
        python app.py
        ```
        *(Note: This might not enable Flask's debug mode unless configured within `app.py`)*

6.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5001`.

## Running with Docker

Containerizing the application ensures it runs consistently across different environments.

### Using Dockerfile

This method builds an image containing the application and its dependencies, but requires a separate Redis instance.

1.  **Build the Docker image:**
    ```bash
    docker build -t system-monitoring-dashboard .
    ```

2.  **Run the Docker container:**
    *Important:* This assumes Redis is accessible from the container (e.g., running on the host network or another container). You might need to configure `REDIS_HOST` environment variable if Redis isn't on `localhost` relative to the *container*. For simplicity, if Redis runs locally on the default port, you can often use `host.docker.internal` on Docker Desktop:
    ```bash
    # Example: Pointing to Redis on the host machine from the container
    docker run -p 5001:5001 \
           -e REDIS_HOST=host.docker.internal \
           -e REDIS_PORT=6379 \
           system-monitoring-dashboard
    ```
    If Redis is also running as a container on a shared Docker network, use its service name as `REDIS_HOST`.

3.  **Access the application:**
    Open your browser and navigate to `http://localhost:5001`.

### Using Docker Compose (Recommended)

Docker Compose simplifies managing multi-container applications (like our Flask app and its Redis dependency).

1.  **Ensure Docker Compose is installed.**

2.  **Start the services:**
    Navigate to the project root directory (where `docker-compose.yml` is located).
    ```bash
    docker-compose up --build
    ```
    This command performs the following:
    -   Builds the `web` service image (if not already built or if changes are detected).
    -   Pulls the official `redis` image.
    -   Creates and starts containers for both `web` (Flask app) and `redis` services.
    -   Connects them on a shared Docker network, allowing the Flask app to reach Redis using the service name `redis`.

3.  **Access the application:**
    Open your browser and navigate to `http://localhost:5001`.

4.  **Stop the services:**
    Press `Ctrl+C` in the terminal where `docker-compose up` is running, then run:
    ```bash
    docker-compose down
    ```
    This stops and removes the containers, network, and volumes (unless specified otherwise).

5.  **Live Reloading (Development):**
    If your `docker-compose.yml` mounts the source code and uses a development server that supports reloading (like Flask's debug mode), you can use `watch` for automatic rebuilding/restarting on file changes:
    ```bash
    docker-compose watch
    ```

## Testing (with Testcontainers)

Integration tests ensure the application interacts correctly with its dependencies like Redis. `Testcontainers` provides lightweight, ephemeral instances of services in Docker containers for testing.

1.  **Install Test Dependencies:**
    ```bash
    pip install pytest testcontainers redis
    ```

2.  **Example Test File (`test_app.py`):**
    Create a file named `test_app.py` (or add to an existing one):
    ```python
    import pytest
    import redis as redis_lib # Renamed to avoid conflict with fixture name
    import os
    from testcontainers.redis import RedisContainer
    from app import app # Assuming your Flask app instance is named 'app' in 'app.py'

    # Fixture to start a Redis container for the test session
    @pytest.fixture(scope="module")
    def redis_container():
        # Use RedisContainer from testcontainers
        with RedisContainer() as redis_c:
            # Get connection details
            redis_host = redis_c.get_container_host_ip()
            redis_port = redis_c.get_exposed_port(6379)

            # Set environment variables for the Flask app to use *during the test*
            os.environ["REDIS_HOST"] = redis_host
            os.environ["REDIS_PORT"] = str(redis_port)

            # Yield connection details for direct use in tests if needed
            yield redis_host, redis_port

            # Clean up environment variables after tests
            del os.environ["REDIS_HOST"]
            del os.environ["REDIS_PORT"]

    # Fixture to provide a test client for the Flask app
    @pytest.fixture
    def client(redis_container): # Depend on redis_container to ensure it's running
        app.config["TESTING"] = True
        # Configure app to use the test Redis instance (if not already done via env vars)
        # app.config['REDIS_HOST'] = os.environ["REDIS_HOST"]
        # app.config['REDIS_PORT'] = int(os.environ["REDIS_PORT"])
        with app.test_client() as client:
            yield client

    # Test 1: Verify direct connection to the Testcontainer Redis
    def test_redis_connection(redis_container):
        redis_host, redis_port = redis_container
        r = redis_lib.Redis(host=redis_host, port=int(redis_port), decode_responses=T rue)
        assert r.ping() # Check connection
        r.set("test_key", "Hello from Testcontainers!")
        assert r.get("test_key") == "Hello from Testcontainers!"

    # Test 2: Verify the /metrics endpoint works and returns expected structure
    def test_metrics_endpoint(client): # Uses the Flask test client
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list) # Expecting a list of metrics
        # Check structure of the latest metric entry if list is not empty
        if data:
             latest_metric = data[0] # Assuming latest is first
             assert "timestamp" in latest_metric
             assert "cpu" in latest_metric
             assert "memory" in latest_metric
             assert "disk" in latest_metric

    # Add more tests as needed (e.g., testing the root '/' endpoint)
    def test_dashboard_loads(client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"System Monitoring Dashboard" in response.data # Check for title in HTML

    ```

3.  **Run the Tests:**
    Ensure Docker is running. Execute pytest from your project's root directory:
    ```bash
    pytest test_app.py
    # Or simply:
    # pytest
    ```
    Pytest will discover and run the tests, starting and stopping the Redis container automatically.

## Advanced Docker Productivity Tools

Leverage these tools to improve your Docker workflow:

### Docker Desktop

-   **Overview:** Provides a user-friendly GUI for managing containers, images, volumes, and networks on macOS and Windows. Great for visual inspection, log viewing, and quick actions.
-   **Usage:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/). Launch it to see your running containers (started via `docker run` or `docker-compose up`), view logs, inspect configurations, and monitor resource usage.

### Docker Build Cloud (using Buildx)

-   **Overview:** Speeds up container image builds, especially for larger projects or in CI/CD pipelines, by utilizing advanced caching and parallel build processing in the cloud or locally.
-   **Usage:**
    ```bash
    # Check Buildx version (usually included with Docker)
    docker buildx version

    # Create a new builder instance (optional, can use default)
    # docker buildx create --name mybuilder --use

    # Build using Buildx (example using default builder)
    # Offers potential caching improvements over standard 'docker build'
    docker buildx build --platform linux/amd64 -t system-monitoring-dashboard --load .
    # Add --push to push directly to a registry after building

    # Using docker bake for more complex multi-platform or multi-target builds (requires a bake file e.g., docker-bake.hcl)
    # docker buildx bake --progress=plain
    ```

### Docker Scout

-   **Overview:** Analyzes your container images for security vulnerabilities (CVEs) and provides remediation advice. Helps maintain a secure software supply chain.
-   **Usage:** (Requires Docker Pro, Team, or Business subscription, or enabling it locally)
    ```bash
    # Get a quick overview of vulnerabilities
    docker scout quickview system-monitoring-dashboard

    # List detailed CVE information
    docker scout cves system-monitoring-dashboard
    ```

### Docker Hub

-   **Overview:** Docker's official cloud-based registry service for finding, storing, and sharing container images.
-   **Steps to Push Your Image:**
    1.  **Log in to Docker Hub:**
        ```bash
        # Enter your username and password/token when prompted
        docker login --username YOUR_DOCKERHUB_USERNAME
        ```
    2.  **Tag your image:** Images need to be tagged with `yourusername/repository:tag`.
        ```bash
        # If you built with 'docker build':
        docker tag system-monitoring-dashboard YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest

        # Or build directly with the tag:
        # docker build -t YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest .
        ```
    3.  **Push the image:**
        ```bash
        docker push YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest
        ```
    Now your image is available on Docker Hub for others to pull or for deployment.

## Summary of Key Commands

| Action                   | Command                                                            | Notes                                       |
| :----------------------- | :----------------------------------------------------------------- | :------------------------------------------ |
| **Install Local Deps**   | `pip install -r requirements.txt`                                  | Run inside activated virtual env            |
| **Run Locally**          | `flask run --host=0.0.0.0 --port=5001`                             | Requires local Redis running                |
| **Build Docker Image**   | `docker build -t system-monitoring-dashboard .`                    | Builds the Flask app image                  |
| **Run Docker Container** | `docker run -p 5001:5001 [options] system-monitoring-dashboard`    | Requires accessible Redis; see options above |
| **Start Docker Compose** | `docker-compose up --build`                                        | Builds (if needed) & starts app + Redis   |
| **Stop Docker Compose**  | `docker-compose down`                                              | Stops and removes containers/network      |
| **Live Reload (Compose)**| `docker-compose watch`                                             | For development with code mounting        |
| **Run Tests**            | `pytest`                                                           | Executes tests using `pytest`               |
| **Build with Buildx**    | `docker buildx build -t system-monitoring-dashboard --load .`      | Potential for faster builds/caching       |
| **Scan Image (Scout)**   | `docker scout quickview system-monitoring-dashboard`               | Checks for vulnerabilities                  |
| **Log in to Docker Hub** | `docker login --username YOUR_DOCKERHUB_USERNAME`                  | Authenticates for push/pull               |
| **Tag Image for Hub**    | `docker tag <local_image> <hub_user>/<repo>:<tag>`                 | Prepares image name for push                |
| **Push to Docker Hub**   | `docker push YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest` | Uploads the tagged image                  |
