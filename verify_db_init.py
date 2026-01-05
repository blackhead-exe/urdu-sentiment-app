from db import supabase_public, supabase_admin
import os
from dotenv import load_dotenv

load_dotenv()

print("--- Supabase Initialization Check ---")
print(f"SUPABASE_URL found: {bool(os.getenv('SUPABASE_URL'))}")
print(f"SUPABASE_ANON_KEY found: {bool(os.getenv('SUPABASE_ANON_KEY'))}")
print(f"SUPABASE_SERVICE_KEY found: {bool(os.getenv('SUPABASE_SERVICE_KEY'))}")

print("\n--- Client Status ---")
if supabase_public:
    print("SUCCESS: supabase_public initialized.")
else:
    print("FAILURE: supabase_public is None.")

if supabase_admin:
    print("SUCCESS: supabase_admin initialized.")
else:
    print("FAILURE: supabase_admin is None.")

print("\n--- Test Public Call ---")
try:
    # Try a simple select to test connection
    res = supabase_public.table("sentiment_logs").select("id").limit(1).execute()
    print("SUCCESS: Public client can query database.")
except Exception as e:
    print(f"FAILURE: Public client query error: {e}")

print("\n--- Test Admin Call ---")
if supabase_admin:
    try:
        # Try an admin-only operation or just a query
        res = supabase_admin.table("sentiment_logs").select("id").limit(1).execute()
        print("SUCCESS: Admin client can query database.")
    except Exception as e:
        print(f"FAILURE: Admin client query error: {e}")
