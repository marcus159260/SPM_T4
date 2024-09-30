from flask import Flask
from routes.user_routes import user_bp
from dotenv import load_dotenv
import os

from flask_cors import CORS


# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api/users/') #url_prefix is the url that you call to see the data

@app.route("/")
def index(): 
    return "Homepage for Website"

if __name__ == '__main__':
    app.run(debug=True)

#-----