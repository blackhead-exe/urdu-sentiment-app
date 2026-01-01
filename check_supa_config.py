import os
from supabase import create_client
from dotenv import load_dotenv
import time
import random

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_ANON_KEY not found in .env")
    exit(1)

supabase = create_client(url, key)

email = f"test.user.{int(time.time())}@gmail.com"
password = "testPassword123!"

print(f"Attempting signup with {email}...")
try:
    res = supabase.auth.sign_up({"email": email, "password": password})
    print("Signup Response User:", res.user)
    print("Signup Response Session:", res.session)
    
    if res.user and res.session is None:
        print("\n[RESULT] Signup successful but NO SESSION. Email confirmation is likely REQUIRED.")
    elif res.user and res.session:
        print("\n[RESULT] Signup successful AND SESSION returned. Email confirmation might be DISABLED.")
    
    print("\nAttempting immediate login...")
    try:
        login_res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        print("Login successful!")
    except Exception as e:
        print(f"\n[RESULT] Login FAILED: {e}")

except Exception as e:
    print(f"Signup FAILED: {e}")
