import streamlit as st
from rembg import remove, new_session
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Tesco AI Studio Pro", layout="wide")

# --- 1. CACHING FOR SPEED ---
@st.cache_resource
def get_rembg_session():
    """Load the model once and keep it in memory."""
    return new_session("u2net") 

def add_branding(background_img, logo_path, text=""):
    """Adds logo and optional campaign text."""
    # 1. Add Logo
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((150, 80))
        background_img.paste(logo, (20, 20), logo)
    except Exception:
        pass # Skip logo if missing

    # 2. Add Text (If user typed any)
    if text:
        draw = ImageDraw.Draw(background_img)
        # Try to load a default font, otherwise use default
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Draw text at the bottom center
        text_position = (50, background_img.height - 80)
        draw.text(text_position, text, fill="black", font=font)

    return background_img

def process_image(uploaded_file, bg_color, campaign_text, session):
    input_image = Image.open(uploaded_file).convert("RGBA")
    
    # Use the cached session for faster removal
    no_bg_image = remove(input_image, session=session)
    
    new_bg = Image.new("RGBA", no_bg_image.size, bg_color)
    new_bg.paste(no_bg_image, (0, 0), no_bg_image)
    
    final_image = add_branding(new_bg, "logo.png", campaign_text)
    return final_image

# --- APP UI ---
st.title("🛍️ Tesco AI Studio: Enterprise Edition")
st.markdown("Batch process product images for marketing campaigns instantly.")

# Sidebar for controls
with st.sidebar:
    st.header("Campaign Settings")
    bg_color = st.color_picker("Background Color", "#FFFFFF")
    campaign_text = st.text_input("Campaign Slogan", "Clubcard Price")
    st.info("Tip: Upload multiple files to process a whole catalog at once.")

# File Uploader (Multiple Files!)
uploaded_files = st.file_uploader("Upload Product Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    session = get_rembg_session() # Load model once
    
    st.divider()
    st.write(f"**Processing {len(uploaded_files)} images...**")
    
    cols = st.columns(3) # Create a grid layout
    
    for i, file in enumerate(uploaded_files):
        with cols[i % 3]: # Cycle through columns
            processed_img = process_image(file, bg_color, campaign_text, session)
            
            st.image(processed_img, caption=file.name, use_container_width=True)
            
            # Individual Download Button
            buf = io.BytesIO()
            processed_img.convert("RGB").save(buf, format="JPEG")
            st.download_button(
                f"Download {file.name}",
                data=buf.getvalue(),
                file_name=f"tesco_{file.name}",
                mime="image/jpeg",
                key=f"dl_{i}"
            )