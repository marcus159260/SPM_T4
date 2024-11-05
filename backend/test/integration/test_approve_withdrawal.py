# import pytest
# import json
# from app import app 
# from util.db import supabase

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client
        
# def test_approve_withdrawal_success(client):
#     request = {
#         "Request_ID": 263
#     }
#     response = client.post("/api/wfh/requests/approvewithdrawal")
#     print(response[0]["error"])
#     assert response.status_code == 200
    
# def test_approve_withdrawal_fail(client):
#     request = {
#     }
#     response = client.post("/api/wfh/requests/approvewithdrawal")
#     assert response.status_code == 400
    
    