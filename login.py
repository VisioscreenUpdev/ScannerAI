import streamlit as st
from streamlit_authenticator import Authenticate
import streamlit as st
import bcrypt


def check_credentials():
    # Hardcoded credentials for demonstration purposes
    st.image("logo.svg")
    PASSWORD = st.secrets["password"]
    print(PASSWORD)
    print("PASSWORD")

    credentials = {
        'usernames': {
            'admin': {
                'name': 'Admin User',
                'password': PASSWORD,  # Hashing 'admin' password
                'email': 'admin@example.com',
            }
        }
    }

    # Instantiate the Authenticate class
    auth = Authenticate(credentials, cookie_name='auth', key='secret_key')

    # Define a function to create the login form
    # Use the login method from the Authenticate class
    name, authentication_status, username = auth.login(location='main')

    # Check if login was successful
    if authentication_status:
        return True
        # Additional logic here for authenticated users
    elif authentication_status == False:
        st.error('Mot de passe incorrect')
        return False
    # For no input, do not display any message

    # Call the login form function to display the form
