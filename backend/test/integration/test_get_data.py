import pytest
import json
from app import app 
import subprocess
import time

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def start_stop_server():
   
    server_process = subprocess.Popen(["python", "backend/app.py"])
    time.sleep(2)
    
    yield server_process

    # Stop the server before the next test
    server_process.terminate()
    server_process.wait()
    time.sleep(2)  # Allow some time for the server to completely stop

def test_get_wfh_requests_success(client, start_stop_server):
    response = client.get('/api/wfh/requests')
    assert response.status_code == 200

def test_get_wfh_requests_no_connection(client):
    response = client.get('/api/wfh/requests')
    assert response.status_code == 500
