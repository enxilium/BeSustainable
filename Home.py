import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="BeSustainable",
    page_icon="🍃",
)

st.write("# Welcome to BeSustainable! 👋")


st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
            
    .stSidebar {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    **BeSustainable is [Insert Description]**

"""
)

image = st.file_uploader("Please upload a picture", type=["csv", "txt", "pdf", "png", "jpg"])

if image is not None:
    try:

        st.write("File uploaded successfully!")
        st.write(f"File name: {image.name}")

        st.image(Image.open(image), use_column_width=True)

    except:
        st.error("File failed to upload. Please try again.")

login, signup = st.sidebar.columns(2)
# Initialize session state variables
if 'show_login' not in st.session_state:
    st.session_state['show_login'] = False
if 'show_signup' not in st.session_state:
    st.session_state['show_signup'] = False

# Define the login and signup logic
with st.sidebar:
    if st.button("Login"):
        st.session_state['show_login'] = True
        st.session_state['show_signup'] = False

    if st.button("Sign Up"):
        st.session_state['show_signup'] = True
        st.session_state['show_login'] = False

# Login section
if st.session_state['show_login']:
    st.write("### Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create columns for buttons
    col1, col2 = st.columns([3, 1])  # Adjust column ratios as needed

    with col1:
        if st.button("Confirm Login"):
            st.write("Login Details:")
            st.write(f"Username: {username}")
            st.write(f"Password: {password}")

    with col2:
        if st.button("Cancel"):
            st.session_state['show_login'] = False

# Sign-up section
if st.session_state['show_signup']:
    st.write("### Sign Up")
    signup_username = st.text_input("Username")
    email = st.text_input("Email")
    signup_password = st.text_input("Password", type="password")

    # Create columns for buttons
    col1, col2 = st.columns([3, 1])  # Adjust column ratios as needed

    with col1:
        if st.button("Confirm Sign Up"):
            st.write("Sign Up Details:")
            st.write(f"Username: {signup_username}")
            st.write(f"Email: {email}")
            st.write(f"Password: {signup_password}")

    with col2:
        if st.button("Cancel"):
            st.session_state['show_signup'] = False