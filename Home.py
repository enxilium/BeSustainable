import streamlit as st
from PIL import Image
import openai
from openai import OpenAI
import os
import tempfile
from dotenv import load_dotenv
import base64
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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


def get_clothing_description(base64_string):
    try:
        # Create a chat completion request with the image URL
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the model that supports vision
            messages=[
                {
                    'role': 'user',
                    'content': [
                        { # {'type', 'brand', 'material', 'style', 'color', 'state'}
                            'type': 'text',
                            'text': """Describe the clothing in the image in the following format: 
                            'type': pick the one that suits the clothing best: dress, shoes, jacket, pants, or simply n/a
                            'brand': the brand should be in all lowercase with all spaces removed
                            'material': choose between leather, cotton, polyester, denim, or simply n/a
                            'style': choose between casual, formal, or athletic
                            'color': describe the color. don't use 'light color' or 'dark color' here
                            'state': the condition of the clothing, choose between used and new
                            Lastyl after 3 %%%, output a choice that you think fits best for this article of clothing, if you had to choose. Do not explain why, simply output your choice.
                            Choose between THRIFT, DONATE, DISPOSE""",
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f"data:image/jpeg;base64,{base64_string}",  # Embed the Base64 string directly
                            },
                        },
                    ],
                }
            ]
        )
        data = response.choices[0].message.content
        st.write(data)
        st.write(data.split('%%%'))
        return data
    except Exception as e:
        st.write(e)
        pass



        

temp_dir = tempfile.TemporaryDirectory()
picture = st.camera_input("Take a picture")

if picture is not None:
    # Read the image data
    image_data = picture.getvalue()
    
    # Convert the image data to a base64 string
    base64_string = base64.b64encode(image_data).decode("utf-8")

    # Display the image
    # st.image(image_data, caption="Captured Image", use_column_width=True)

    # Show the base64 string
    st.write("Base64 String for API access:")
    st.text(base64_string)  # Display as text or use it in your API call
    st.write(get_clothing_description(base64_string))


# image = st.file_uploader("Please upload a picture", type=["csv", "txt", "pdf", "png", "jpg"])

# if image is not None:
#     try:

#         st.write("File uploaded successfully!")
#         st.write(f"File name: {image.name}")

#         st.image(Image.open(image), use_column_width=True)

#     except:
#         st.error("File failed to upload. Please try again.")


if picture is not None:
    try:
        st.write("Picture taken successfully!")
        st.write(f"File name: {picture.name}")

        # Display the image
        # st.image(Image.open(picture), use_column_width=True)

        # Save picture temporarily for processing
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(picture.getbuffer())

        # Get clothing description from ChatGPT
        # detailed_description = get_clothing_description(base64_string)
        # if detailed_description:
        #     st.write("Detailed Clothing Description:")
        #     st.write(detailed_description)

    except Exception as e:
        st.error(f"File failed to upload. Please try again. Error: {e}")
# elif image is not None:
#     try:
#         st.write("File uploaded successfully!")
#         st.write(f"File name: {image.name}")

#         # Display the image
#         st.image(Image.open(image), use_column_width=True)

#         # Save image temporarily for processing
#         temp_image_path = "temp_image.jpg"
#         with open(temp_image_path, "wb") as f:
#             f.write(image.getbuffer())

#         # Get clothing description from ChatGPT
#         detailed_description = get_clothing_description(temp_image_path)
#         if detailed_description:
#             st.write("Detailed Clothing Description:")
#             st.write(detailed_description)

#     except Exception as e:
#         st.error(f"File failed to upload. Please try again. Error: {e}")



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
        if st.button("Cancel Login"):
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
        if st.button("Cancel Signup"):
            st.session_state['show_signup'] = False