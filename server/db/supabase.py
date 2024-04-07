from supabase import Client, create_client
from dotenv import load_dotenv
import os

load_dotenv()

url: str = os.environ['SUPABASE_URL']
key: str = os.environ['SUPABASE_KEY']

def create_supabase_client():
    supabase: Client = create_client(url, key)
    return supabase