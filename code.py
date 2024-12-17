import streamlit as st
from PIL import Image
import base64
import openai
import os
from io import BytesIO

DEFAULT_API_KEY = '***'

import streamlit as st
from PIL import Image
import openai
import base64
from io import BytesIO

# --- CONFIGURABLE API KEY INPUT ---

# Streamlit UI Title
st.title("Grocery Product Image Classifier")

# Sidebar for Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", value=DEFAULT_API_KEY, type="password")
prompt_text = st.sidebar.text_area("Custom Prompt", 
                                  value="You are a grocery image classifier. Classify the image across grocery categories like Fruits, Meat, Dairy, etc. If it does not match, return 'Other'.")

grocery_categories = [
    "Fruits and Vegetables", "Meat and Poultry", "Dairy Products", "Beverages", "Bakery Items",
    "Snacks", "Frozen Foods", "Canned Goods", "Seafood", "Condiments and Sauces", "Healthy Food", "Energy Drinks"
]

def classify_image(image_data, prompt):
    """
    Send the image and prompt to the OpenAI GPT-4 Vision model for classification.
    """
    # Encode the image to base64
    buffered = BytesIO()
    image_data.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Send request to OpenAI
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "Classify the grocery item in the image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                ]}
            ],
            max_tokens=500,
            temperature=0,
            top_p=1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- IMAGE UPLOAD ---
uploaded_file = st.file_uploader("Upload an image of the product", type=["jpg", "jpeg", "png", "bmp", "webp"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Classify button
    if st.button("Classify Image"):
        if not api_key:
            st.error("Please provide a valid OpenAI API key.")
        else:
            openai.api_key = api_key  # Set API key dynamically
            st.info("Classifying the image...")
            
            # Get the result from GPT Vision
            result = classify_image(image, prompt_text)
            st.success(f"**Category:** {result}")
            
            # Optionally show the categories
            st.subheader("Grocery Store Categories")
            st.write(', '.join(grocery_categories))
else:
    st.write("Please upload an image to proceed.")
