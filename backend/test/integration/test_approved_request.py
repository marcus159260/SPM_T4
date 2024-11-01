import pytest
import json
from app import app 
from util.db import supabase

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
# def test_approve_request_success(client):
#     # Get an actual pending request
#     request = {
#         "Request_ID" = 247,
#         "request_Status" = "Pending",
        
#     }
    # approve it
    # then reset the status to pending