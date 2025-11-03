import hashlib
import Database
import streamlit as st
import Authenticator
import Analyzer


def login_page():
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
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")

def dashboard_page():
    st.title(f"Welcome, {st.session_state.username}!")

    if st.button("Refresh Data"):
        with st.spinner("Fetching latest market data..."):
            st.session_state.df = Analyzer.get_dataframe()

    if 'df' not in st.session_state:
        with st.spinner("Fetching initial market data..."):
            st.session_state.df = Analyzer.get_dataframe()

    df = st.session_state.df
    
    if not df.empty:
        st.subheader("Market Data")
        st.dataframe(df)

        deals = Analyzer.find_deals(df)

        if not deals.empty:
            st.subheader("Found Deals")
            st.dataframe(deals)
        else:
            st.info("No outstanding deals found based on current criteria.")
    else:
        st.warning("Could not fetch market data. The API might be down or your key is invalid.")


def main():
    Database.init_db()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page()


if __name__ == "__main__":
    main()
