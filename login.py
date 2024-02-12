import streamlit as st

# Hardcoded user credentials
PASSWORD = st.secrets["password"]


# Function to check if the entered credentials match the hardcoded ones
def check_credentials(username, password):
    return password == PASSWORD

# Creating a simple login form
def page():
    st.title('Login Page')

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.write("## Login Here")

        # User inputs for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Login button
        if st.button('Login'):
            # Check if credentials are correct
            if check_credentials(username, password):
                st.success('Login Successful!')
                # You can add your app's main functions here
                st.session_state['authenticated'] = True
                st.experimental_rerun()
            else:
                st.error('Incorrect Username/Password')


