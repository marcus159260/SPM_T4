from flask import Flask
from routes.user_routes import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api/users/')

@app.route("/")
def index(): 
    return "Homepage for Website"

if __name__ == '__main__':
    app.run(debug=True)
