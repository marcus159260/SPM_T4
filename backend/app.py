from flask import Flask, jsonify
from routes.user_routes import user_bp
from routes.requests import wfh_bp
from routes.auth import auth_bp
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config import Config
from flask_session import Session

# Load environment variables from the .env file
load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)

Session(app)

# {"origins": "https://spm-t4.vercel.app"}
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}},expose_headers=['staff_id','role'])

app.register_blueprint(auth_bp, url_prefix='/api/auth/')
app.register_blueprint(user_bp, url_prefix='/api/users/') #url_prefix is the url that you call to see the data
app.register_blueprint(wfh_bp, url_prefix='/api/wfh/') #to see requests data

@app.route("/")
def index(): 
    return "Homepage for Website"

    
if __name__ == '__main__':
    app.run(debug=True)
