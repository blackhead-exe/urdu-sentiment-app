import streamlit as st
from db import supabase_public, supabase_admin

#def login(email, password):
   # res = supabase_public.auth.sign_in_with_password({
    #    "email": email,
     #   "password": password
    #})
    #if not res.session:
    #    raise Exception("Invalid credentials or email not verified")
    #    #return res
def login(email, password):
    res = supabase_public.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    print("AUTH RESPONSE:", res)
    return res


def signup(email, password):
    try:
        # Attempt to create user with auto-confirmation using admin client
        return supabase_admin.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True
        })
    except Exception as e:
        print(f"Admin signup failed: {e}")
        return supabase_public.auth.sign_up({
            "email": email,
            "password": password
        })
    

def logout():
    supabase_public.auth.sign_out()
    st.session_state.clear()
