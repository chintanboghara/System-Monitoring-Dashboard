# System Monitoring Dashboard

**System Monitoring Dashboard** is a Flask-based web application that displays real-time system metrics, CPU, memory, and disk usage—and stores the last five metrics in Redis.

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

   Alternatively, run:

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

   Open your browser and go to [http://localhost:5001](http://localhost:5001).

### Using Docker Compose

1. **Ensure Docker Compose is installed.**

2. **Start the services:**

   ```bash
   docker-compose up
   ```

   This command builds and starts both the Flask web service and the Redis service.

3. **Access the application:**

   Open your browser and navigate to [http://localhost:5001](http://localhost:5001).
