from flask import Flask
from routes.user_routes import user_bp
from routes.requests import wfh_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app = Flask(__name__)
CORS(app,resources={r"/*":{'origins':"*"}})

app.register_blueprint(user_bp, url_prefix='/api/users/')
app.register_blueprint(wfh_bp, url_prefix='/api/wfh/')


@app.route("/")
def index(): 
    return "Homepage for Website"

if __name__ == '__main__':
    app.run(debug=True)
