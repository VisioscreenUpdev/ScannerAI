import streamlit as st

# Hardcoded user credentials
PASSWORD = st.secrets["password"]


# Function to check if the entered credentials match the hardcoded ones
def check_credentials(username, password):
    return password == PASSWORD

# Creating a simple login form
def page():
    st.image("logo.svg")

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.title("Connexion")

        # User inputs for username and password
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")

        # Login button
        if st.button('Se connecter'):
            # Check if credentials are correct
            if check_credentials(username, password):
                st.success('Login Successful!')
                # You can add your app's main functions here
                st.session_state['authenticated'] = True
                st.experimental_rerun()
            else:
                st.error('Mot de passe incorrect')


