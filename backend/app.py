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

@app.route("/api/requests", methods=['GET'])
def get_requests():
    # Use the Supabase client to fetch data
    response = supabase.table('request').select("*").execute()

    # Check for successful response
    if response.data is not None:
        return jsonify(response.data), 200
    else:
        # If there's an error, return the error message
        return jsonify({"error": response.error}), 400
    
if __name__ == '__main__':
    app.run(debug=True)
