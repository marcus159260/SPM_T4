from flask import Flask, jsonify
from routes.user_routes import user_bp
from flask_cors import CORS

from util.db import supabase

app = Flask(__name__)
CORS(app,resources={r"/*":{'origins':"*"}})

app.register_blueprint(user_bp, url_prefix="/users")

@app.route("/")
def index(): 
    return "Homepage for Website"

@app.route("/api/requests/<int:staff_id>", methods=['GET'])
def get_requests_by_staff(staff_id):
    # Use the Supabase client to fetch data
    print(f"Fetching requests for Staff ID: {staff_id}")
    response = supabase.rpc('get_staff_requests', {'p_staff_id': staff_id}).execute()
    print(f"Supabase Response: {response}")
    # Check for successful response
    if response.data is not None:
        print(f"Response Data: {response.data}")
        return jsonify(response.data), 200
    else:
        # If there's an error, return the error message
        print(f"Error occurred: {response.error}")
        return jsonify({"error": "No data found or request failed", "details": response.error}), 400
    
if __name__ == '__main__':
    app.run(debug=True)
