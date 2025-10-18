import sqlite3
import hashlib
import Database
import streamlit as st
import Authenticator


  

if __name__ == "__main__":
    Database.init_db()

    option = st.radio("Select option:", ["Login", "Sign Up"])

    if option == "Sign Up":
        st.subheader("Create a new account")
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif Database.insert_user(new_username, new_email, password_hash):
                st.success("Account created successfully! You can now log in.")
            else:
                st.error("Username or email already exists")

    elif option == "Login":
        st.subheader("Login to your account")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if Authenticator.verify_user(username, password):
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password")
            
