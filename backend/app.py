from flask import Flask, jsonify
from routes.user_routes import user_bp
from routes.requests import wfh_bp
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


app = Flask(__name__)
CORS(app,resources={r"/*":{'origins':"*"}})


app.register_blueprint(user_bp, url_prefix='/api/users/') #url_prefix is the url that you call to see the data
app.register_blueprint(wfh_bp, url_prefix='/api/wfh/') #to see requests data

@app.route("/")
def index(): 
    return "Homepage for Website"
    
if __name__ == '__main__':
    app.run(debug=True)
