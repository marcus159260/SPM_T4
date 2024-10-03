import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL or Key is missing")


supabase: Client = create_client(url, key)
