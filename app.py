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
#st.title("Sadhya നിരൂപണം AI")
st.write("Warning: This AI has zero chill. Your sadya will get roasted 🍽️🔥")

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
    You are a strict but funny sadya critic.  
    A user uploads a photo of their banana leaf Sadya. Your job is to analyze it with both accuracy and humor.

    Reference Rules (traditional Sadya placement):
    - Starters (sweet banana chips, salted banana chips) → extreme top left.
    - Pickles → right of chips.
    - Ripe banana → extreme bottom left.
    - Papadam → next to the banana.
    - Curries on top row (from left to right, after pickles): inji-puli, olan, kaalan, thoran, mezhukkupuratti, koottu curry, aviyal, erissery, pulisseri, pachadi, kichadi, and finally theeyal at the top right.
    - Parippu curry + ghee → bottom right.
    - Rice → center of the leaf.
    - Payasam → served last, usually in a small spot or cup.

    How to reply:  
    - Roast in simple English, no big words.  
    - Point out mistakes sharply, don’t be nice.  
    - Use sarcasm and 2–3 emojis.  
    - 7-8 sentences only.  
    - End with a final burn.   
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
    