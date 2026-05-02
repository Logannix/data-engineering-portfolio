import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(st.secrets["postgresql://neondb_owner:npg_TlcE4D5pjLOz@ep-weathered-mouse-abqopvns-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"])