# System Monitoring Dashboard

**System Monitoring Dashboard** is a lightweight Flask web application that provides real-time insights into your system's performance by displaying key metrics such as CPU, memory, and disk usage. It is designed for developers, system administrators, or anyone interested in monitoring their system's resource utilization. The dashboard leverages Redis to store the five most recent metric readings, offering a brief historical snapshot of system performance. With automatic refreshes every 5 seconds, you can stay updated on your system's health without manual intervention.

The application is built for easy deployment, either locally for development or containerized using Docker and Docker Compose, integrating seamlessly with advanced Docker productivity tools.

<!-- Consider adding a screenshot or GIF here -->
<!-- ![Dashboard Screenshot](link/to/your/screenshot.png) -->

## Features

-   **Real-time Metrics:** Displays current CPU usage (%), memory usage (%), and disk usage (%) with updates every 5 seconds for up-to-date insights.
-   **Data Persistence:** Stores the five most recent metric snapshots in Redis, allowing you to view a brief history of system performance.
-   **Live Dashboard:** The frontend automatically fetches and updates metrics every 5 seconds without requiring page reloads, ensuring a smooth user experience.
-   **Containerized:** Ready for deployment using Docker and Docker Compose, ensuring consistent environments across development and production.
-   **Cross-Platform:** Uses the `psutil` library to gather system metrics, making it compatible with Linux, macOS, and Windows.

## Tech Stack

-   **Backend:** Python with Flask – chosen for its simplicity and ease of use in building lightweight web applications.
-   **Data Store:** Redis – an in-memory data store that provides fast access to recent metrics.
-   **System Metrics:** `psutil` library – a cross-platform tool for retrieving system information.
-   **Frontend:** HTML, CSS, JavaScript (Fetch API) – for a responsive and dynamic user interface.
-   **Containerization:** Docker and Docker Compose – for consistent deployment and easy management of multi-service applications.

## Getting Started

### Prerequisites

-   **Local Development:**
    -   Python 3.9 or higher
    -   `pip` (Python package installer)
    -   Redis Server ([Installation instructions](https://redis.io/download)) running locally on `localhost:6379`. Start Redis with `redis-server` if it’s not already running.
    -   Git
-   **Containerized Deployment:**
    -   [Docker Engine](https://www.docker.com/get-started)
    -   [Docker Compose](https://docs.docker.com/compose/install/) (v2 recommended)

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chintanboghara/System-Monitoring-Dashboard.git
    cd System-Monitoring-Dashboard
    ```

2.  **Set up a virtual environment (Recommended):**
    *Why?* Isolates project dependencies, preventing conflicts with system-wide packages.
    ```bash
    python3 -m venv venv
    # Activate the environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Command Prompt):
    venv\Scripts\activate
    # On Windows (PowerShell):
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note:* If you encounter issues installing `psutil`, ensure you have the necessary build tools for your platform.

4.  **Ensure Redis is running:**
    Start Redis with `redis-server` and verify the connection using `redis-cli ping` (should return `PONG`).

5.  **Run the Flask application:**
    Use the following command to start the app in development mode:
    ```bash
    flask run --host=0.0.0.0 --port=5001
    ```
    *Note:* Running with `--host=0.0.0.0` makes the app accessible from your local network.

6.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5001`.

## Running with Docker

Containerizing the application ensures it runs consistently across different environments. Below are two methods: using a Dockerfile or Docker Compose (recommended).

### Using Dockerfile

This method builds an image for the Flask app but requires a separate Redis instance.

1.  **Build the Docker image:**
    ```bash
    docker build -t system-monitoring-dashboard .
    ```

2.  **Run the Docker container:**
    *Important:* If Redis is running on your host machine, use `host.docker.internal` as the Redis host. If Redis is in another container, use its service name.
    ```bash
    docker run -p 5001:5001 \
           -e REDIS_HOST=host.docker.internal \
           -e REDIS_PORT=6379 \
           system-monitoring-dashboard
    ```

3.  **Access the application:**
    Open your browser and navigate to `http://localhost:5001`.

### Using Docker Compose (Recommended)

Docker Compose manages both the Flask app and Redis in a single command, simplifying setup.

1.  **Ensure Docker Compose is installed.**

2.  **Start the services:**
    Navigate to the project root directory and run:
    ```bash
    docker-compose up --build
    ```
    This command:
    -   Builds the Flask app image (if needed).
    -   Pulls the official Redis image.
    -   Starts both services, connecting them via a shared Docker network.

3.  **Access the application:**
    Open your browser and navigate to `http://localhost:5001`.

4.  **Stop the services:**
    Press `Ctrl+C` in the terminal, then run:
    ```bash
    docker-compose down
    docker-compose down --rmi all
    ```

5.  **Live Reloading (Development):**
    If your `docker-compose.yml` mounts the source code, use:
    ```bash
    docker-compose watch
    ```
    This enables automatic rebuilding and restarting on file changes.

## Testing (with Testcontainers)

Integration tests ensure the application interacts correctly with Redis. `Testcontainers` provides ephemeral Redis instances for testing.

1.  **Install Test Dependencies:**
    ```bash
    pip install pytest testcontainers redis
    ```

2.  **Run the Tests:**
    Ensure Docker is running, then execute:
    ```bash
    pytest
    ```
    *What it does:* Starts a temporary Redis container, runs tests to verify Redis connection and metrics endpoint, then cleans up.

## Advanced Docker Productivity Tools

Enhance your Docker workflow with these tools:

### Docker Desktop

-   **Overview:** A GUI for managing containers, images, volumes, and networks on macOS and Windows. Ideal for visual inspection, log viewing, and resource monitoring.
-   **Usage:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/). Use it to manage your running containers and services.

### Docker Build Cloud (using Buildx)

-   **Overview:** Accelerates container image builds with advanced caching and parallel processing, especially useful for larger projects or CI/CD pipelines.
-   **Usage:**
    ```bash
    docker buildx build --platform linux/amd64 -t system-monitoring-dashboard --load .
    ```

### Docker Scout

-   **Overview:** Analyzes container images for security vulnerabilities (CVEs) and provides remediation advice.
-   **Usage:** (Requires Docker Pro, Team, or Business subscription)
    ```bash
    docker scout quickview system-monitoring-dashboard
    ```

### Docker Hub

-   **Overview:** Docker's official registry for storing and sharing container images.
-   **Steps to Push Your Image:**
    1.  **Log in to Docker Hub:**
        ```bash
        docker login --username YOUR_DOCKERHUB_USERNAME
        ```
    2.  **Tag your image:**
        ```bash
        docker tag system-monitoring-dashboard YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest
        ```
    3.  **Push the image:**
        ```bash
        docker push YOUR_DOCKERHUB_USERNAME/system-monitoring-dashboard:latest
        ```

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
