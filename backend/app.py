from flask import Flask
from routes.user_routes import user_bp
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the Supabase URL and keys
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Now you can use these variables in your application
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api/users/')

@app.route("/")
def index(): 
    return "Homepage for Website"

if __name__ == '__main__':
    app.run(debug=True)
