import streamlit as st
from PIL import Image
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import joblib
import ast
import pandas as pd

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.set_page_config(
    page_title="EcoCloset",
    page_icon="🍃",
)

st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
            
    .stSidebar {
        background-color: white;
    }

    .center-text {
        text-align: center;
    }

    .camera-box {
        border: 2px solid green;
        border-radius: 15px;
        width: 100%;
        padding: 10px;
    }
    
    .centered-content {
        display: flex;
        flex-direction: column; /* Stack items vertically */
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .green-text {
        color: green; /* Set text color to green */
    }

    .full-width-table {
        border-collapse: collapse; /* Collapse borders */
    }
    </style>
    """, unsafe_allow_html=True)


st.write("# <span style='color:green'>Eco</span>Closet 🍃", unsafe_allow_html=True)

col1, col2 = st.columns(2)
logo = Image.open("assets/logo.png")
with col1:
    st.image(logo, width = 300)
with col2:
    st.markdown(
    """<centered-content>**You give us a picture of your <em>worn clothes</em>,\nwe'll give it a <span style='color:green'>second life</span>.**</centered-content>""", unsafe_allow_html=True)


def predict_price(input_data):
    rf_model = joblib.load('model/random_forest_model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    model_columns = joblib.load('model/model_columns.pkl')

    # Define a sample input (type, brand, material, style, color, state)
    input_dict = {
        'type': [input_data[0]],
        'brand': [input_data[1]],
        'material': [input_data[2]],
        'style': [input_data[3]],
        'color': [input_data[4]],
        'state': [input_data[5]]
    }

    data_df = pd.DataFrame(input_dict)
    st.write("### More info about your article of clothing: ")
    st.write(data_df.to_html(classes='full-width-table', index=False), unsafe_allow_html=True)
    
    input_df = pd.DataFrame(input_dict)
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
    input_scaled = scaler.transform(input_encoded)
    predicted_price = rf_model.predict(input_scaled)

    
    return predicted_price[0]


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
                            'color': describe the clothing using 1 color. don't use 'light color' or 'dark color' here.
                            'state': the condition of the clothing, choose between used and new
                            Aftewards, output %%% and then place the descriptions in a list with the following order ['type', 'brand', 'material', 'style', 'color', 'state']. Do not output this string as is. Replace the values within it.
                            Output %%% once again, and then output a choice that you think fits best for this article of clothing, if you had to choose. Do not explain why, simply output your choice.
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
        # st.write(data)
       # Split the input data
        data = data.split('%%%')

        # Predict the price using the second part of the data
        price = predict_price(ast.literal_eval(data[1]))

        # Display the designation with the first three letters in green
        st.markdown('<div class="centered-content">Designation:</div>', unsafe_allow_html=True)

        # Use a span to color the first three letters green
        st.markdown(
            '<div class="centered-content">'
            '<span class="green-text" style="font-size: 40px;">{}</span></div>'.format(data[2]), 
            unsafe_allow_html=True
        )


        # Display the value
        st.markdown('<div class="centered-content">Value:</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="centered-content">'
            '<span class="green-text" style="font-size: 40px;">${}</span></div>'.format(str(round(price, 2))), 
            unsafe_allow_html=True
        )
        
        pass
        # return data
    except Exception as e:
        st.write(e)
        pass


# Create the camera input and wrap it in a div for styling
st.write("### <div class='camera-box'>Photograph Your Clothing</div>", unsafe_allow_html=True); picture = st.camera_input('Webcam permissions required')

if picture is not None:
    # Read the image data
    image_data = picture.getvalue()
    
    # Convert the image data to a base64 string
    base64_string = base64.b64encode(image_data).decode("utf-8")

    # Display the image
    # st.image(image_data, caption="Captured Image", use_column_width=True)

    # Show the base64 string
    # st.write("Base64 String for API access:")
    # st.text(base64_string)  # Display as text or use it in your API call
    get_clothing_description(base64_string)


st.write("### <div class='camera-box'>Upload an Image</div>", unsafe_allow_html=True); image = st.file_uploader('Drag and drop your file here, or click \'Browse Files\'', type=["jpeg"])

if image is not None:
    try:
        image_data = picture.getvalue()
        base64_string = base64.b64encode(image_data).decode("utf-8")
        # st.write("Base64 String for API access:")
        # st.text(base64_string)
        get_clothing_description(base64_string)
    except:
        st.error("File failed to upload. Please try again.")


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
elif image is not None:
    try:
        # st.write("File uploaded successfully!")
        # st.write(f"File name: {image.name}")

        # Display the image
        # st.image(Image.open(image), use_column_width=True)

        # Save image temporarily for processing
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(image.getbuffer())

        # Get clothing description from ChatGPT
        # detailed_description = get_clothing_description(temp_image_path)
        # if detailed_description:
        #     st.write("Detailed Clothing Description:")
        #     st.write(detailed_description)

    except Exception as e:
        st.error(f"File failed to upload. Please try again. Error: {e}")



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