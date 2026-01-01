import sys
import os
import time
from auth import signup, login

# Ensure we can import auth
sys.path.append(os.getcwd())

email = f"verify_fix_{int(time.time())}@test.com"
password = "password123"

print(f"Testing Auth Flow for {email}...")

# 1. Signup
print("Calling signup()...")
try:
    s_res = signup(email, password)
    print("Signup result user:", s_res.user.id)
except Exception as e:
    print(f"Signup FAILED: {e}")
    exit(1)

# 2. Login
print("Calling login()...")
try:
    l_res = login(email, password)
    if l_res.session:
        print("Login SUCCESS! Session obtained.")
    else:
        print("Login Failed: No session.")
except Exception as e:
    print(f"Login Exception: {e}")
