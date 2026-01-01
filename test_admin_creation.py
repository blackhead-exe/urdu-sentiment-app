import os
from supabase import create_client
from dotenv import load_dotenv
import time

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

admin = create_client(url, key)

email = f"auto_confirm_{int(time.time())}@test.com"
password = "password123"

print(f"Creating user {email} via admin...")
try:
    # parameters might need to be passed as a dictionary or kwargs depending on library version
    # Trying dict first common in py libraries
    res = admin.auth.admin.create_user({
        "email": email,
        "password": password,
        "email_confirm": True
    })
    print("User created:", res.user.id)
    print("Confirmed at:", res.user.email_confirmed_at)
    
    print("Attempting login (public)...")
    public = create_client(url, os.getenv("SUPABASE_ANON_KEY"))
    login_res = public.auth.sign_in_with_password({"email": email, "password": password})
    print("Login successful! Session:", login_res.session is not None)

except Exception as e:
    print(f"Failed: {e}")
