import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


response = (
    supabase.table("test_data")
    .select("*")
    .execute()
)


response = (
    supabase.table("test_data")
    .insert({"id": 3, "name": "Hello_3"})
    .execute()
)

response = (
    supabase.table("test_data")
    .select("*")
    .execute()
)

print(response)

