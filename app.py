from flask import Flask, render_template, jsonify
import psutil
import datetime
import redis
import os
import json

app = Flask(__name__)

# Get Redis host & port from environment variables (use defaults for local)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Connect to Redis
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()  # Test connection
except redis.exceptions.ConnectionError:
    app.logger.warning("Redis is not running! The app will work, but metrics won't be saved.")
    redis_client = None

def get_system_metrics():
    """Collect system metrics and store in Redis as JSON."""
    metrics = {
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    }

    if redis_client:
        # Save the metrics as a JSON string and keep only the last 5 records
        redis_client.lpush("metrics", json.dumps(metrics))
        redis_client.ltrim("metrics", 0, 4)
    return metrics

def get_latest_metrics():
    """Retrieve the most recent metrics from Redis if available; otherwise, generate new metrics."""
    if redis_client:
        metrics_list = redis_client.lrange("metrics", 0, -1)
        if metrics_list:
            # The first element is the latest
            return json.loads(metrics_list[0])
    return get_system_metrics()

@app.route('/')
def index():
    # Pass the latest metric to the template
    latest_metrics = get_latest_metrics()
    return render_template('index.html', metrics=latest_metrics)

@app.route('/metrics')
def metrics():
    return jsonify(get_system_metrics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
