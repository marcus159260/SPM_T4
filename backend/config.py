import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# print(f"Supabase URL: {url}")
# print(f"Supabase Key: {key}")

if not url or not key:
    raise ValueError("Supabase URL or Key is missing")

supabase: Client = create_client(url, key)
