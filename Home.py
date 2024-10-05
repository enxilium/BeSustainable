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
        background-color: lightgreen;
    }
            
    .stSidebar {
        background-color: lightgreen;
    }
            
    .stSidebar {
            background-color: lightgreen;
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

with login:
    st.button("Login")

with signup:
    st.button("Sign Up")