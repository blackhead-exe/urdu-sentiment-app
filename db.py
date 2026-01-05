import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# URLs and Keys
url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_ANON_KEY")

# Admin key can be under several names
admin_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize Public Client
if url and anon_key:
    supabase_public = create_client(url, anon_key)
else:
    print("Warning: SUPABASE_URL or SUPABASE_ANON_KEY missing. Public client not initialized.")
    supabase_public = None

# Initialize Admin Client
if url and admin_key:
    supabase_admin = create_client(url, admin_key)
else:
    print("Warning: Admin key (SUPABASE_KEY/SERVICE_KEY) missing. Admin client not initialized.")
    supabase_admin = None