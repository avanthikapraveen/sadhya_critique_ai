import streamlit as st
import os
from PIL import Image
import io
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
st.set_page_config(page_title="Sadhya നിരൂപണം AI",layout="centered")
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=160)
st.title("Sadhya നിരൂപണം AI")
st.write("Upload a photo of your Sadhya and get a friendly, witty critique!")

uploaded_file = st.file_uploader("Upload your Sadhya photo (jpg/png):", type=["jpg", "jpeg", "png"])

@st.cache_data
def resize_image(image_bytes, max_size=1600):  #raw image bytes → shrink it nicely → convert to JPEG → give back raw JPEG bytes
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((max_size,max_size),Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=85)
    return buf.getvalue()

def critique_sadhya(image_bytes):
    model = genai.GenerativeModel("gemini-1.5-flash")
    img = Image.open(io.BytesIO(image_bytes))
    prompt = """
    You are an Onam Sadhya food critic.
    Look at the photo of this banana leaf meal (sadhya) and give a witty critique.
    - Mention placement of dishes, missing items, or funny details.
    - Tone should be humorous but friendly, like teasing a friend during Onam.
    - Keep response short (3–5 sentences).
    """
    response = model.generate_content([prompt, img])
    return response.text

if uploaded_file:
    image_bytes = uploaded_file.read()
    display_bytes = resize_image(image_bytes, max_size=1200)
    st.image(display_bytes, caption="Your Sadhya", width="stretch")
    if st.button("Critique my Sadhya!"):
        with st.spinner("Analyzing your Sadhya..."):
            critique = critique_sadhya(image_bytes)
        st.success("Here's your critique:")
        st.write(critique)
    