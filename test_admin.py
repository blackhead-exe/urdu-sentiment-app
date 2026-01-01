import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY") # Suspected service role key

if not key:
    print("No SUPABASE_KEY found.")
    exit()

try:
    admin = create_client(url, key)
    # Try to list users (admin only operation)
    users = admin.auth.admin.list_users()
    print("Admin access CONFIRMED. User count:", len(users))
except Exception as e:
    print(f"Admin access FAILED: {e}")
