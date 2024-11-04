import pytest
import subprocess
import time
import psutil
import requests

from app import app

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def start_server():
    # Start the server as a subprocess
    server_process = subprocess.Popen(["python", "backend/app.py"])
    time.sleep(2)  # Give some time for the server to start
    return server_process

def stop_server(server_process):
    # Terminate and forcefully kill the server process if it’s still running
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()
        server_process.wait()

    # Confirm the server is down
    if psutil.pid_exists(server_process.pid):
        raise RuntimeError("Server did not stop in a timely manner")

def test_get_wfh_requests_success(client):
    # Start the server
    server_process = start_server()
    
    # Perform the test while server is running
    response = client.get('/api/wfh/requests')
    assert response.status_code == 200

    # Stop the server after the test
    stop_server(server_process)

def test_get_wfh_requests_no_connection():
    # Ensure the server is down by making a real HTTP request
    try:
        response = requests.get("http://127.0.0.1:5000/api/wfh/requests")
        # If the server is down, we should not get a response
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        # Expected outcome, server is unreachable
        pass
