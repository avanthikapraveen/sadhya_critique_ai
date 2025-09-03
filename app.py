import streamlit as st
import os
from PIL import Image
import io

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

def dummy_critique():
    return (
        "Offline mock critique:\n"
        "- Payasam looks very friendly with achar — brave combo! 😅\n"
        "- Papadam is hiding at the leaf edge.\n"
        "- Overall: 8/10 for effort, 9/10 for coconut usage. 🌴"
    )

if uploaded_file:
    image_bytes = uploaded_file.read()
    display_bytes = resize_image(image_bytes, max_size=1200)
    st.image(display_bytes, caption="Your Sadhya", use_container_width=True)
    if st.button("Critique my Sadhya!"):
        st.write(dummy_critique())
    