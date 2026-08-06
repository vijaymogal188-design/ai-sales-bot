import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="AgentFlow AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #0f172a; }
    .hero-title { font-size: 42px; font-weight: 800; text-align: center; margin-bottom: 20px; }
    .hero-title span { color: #7c3aed; }
</style>
""", unsafe_allow_html=True)

query_params = st.query_params
is_admin_url = query_params.get("admin") == "true"

st.sidebar.markdown("### AgentFlow AI")
nav_options = ["Home", "Pricing", "Contact", "Customer Login / Signup"]

if is_admin_url:
    nav_options.append("Admin CRM Dashboard")

nav_choice = st.sidebar.radio("Navigation", nav_options)

if nav_choice == "Home":
    st.markdown('<div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div>', unsafe_allow_html=True)
    st.write("Welcome to the official enterprise portal.")

elif nav_choice == "Pricing":
    st.header("Pricing Plans")
    st.write("Starter: Rs 999 | Pro: Rs 2,999 | Premium: Rs 7,999")

elif nav_choice == "Contact":
    st.header("Contact Us")
    st.text_input("Your Name")
    st.text_area("Your Message")
    st.button("Send Message")

elif nav_choice == "Customer Login / Signup":
    st.header("Customer Portal")
    user = st.text_input("Username or Email")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user and pwd:
            st.success("Login Successful!")
        else:
            st.warning("Please fill details.")

elif nav_choice == "Admin CRM Dashboard":
    if not is_admin_url:
        st.error("404 - Page Not Found / Access Denied")
    else:
        st.header("Admin CRM Dashboard (Secret Secure)")
        st.write("Welcome Admin! All system leads and users data will appear here.")
