import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

supabase: Client = create_client(url, key)
