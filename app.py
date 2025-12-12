import streamlit as st
from rembg import remove, new_session
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tesco Studio | Enterprise",
    layout="wide",
    page_icon="🛍️",
    initial_sidebar_state="expanded"
)

# --- 2. ENTERPRISE CSS (VISIBILITY FIX) ---
st.markdown("""
<style>
    /* FORCE LIGHT MODE FOR ENTIRE APP */
    .stApp {
        background-color: #F8F9FA;
        color: #333333;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
    
    /* FIX INVISIBLE HEADERS (Crucial) */
    h1, h2, h3, h4, h5 {
        color: #00539F !important; /* Tesco Blue */
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    /* FIX INVISIBLE LABELS & TEXT */
    .stMarkdown p, .stMarkdown label, .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #333333 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
    }
    
    /* BUTTONS */
    .stButton>button { 
        background-color: #EE1C2E; color: white; border: none; height: 50px; 
        font-weight: 700; border-radius: 4px; width: 100%; transition: 0.3s; 
    }
    .stButton>button:hover { background-color: #CC0000; box-shadow: 0 4px 12px rgba(238, 28, 46, 0.3); }
    
    /* COMPLIANCE BADGES */
    .badge-pass { background: #E6F4EA; color: #1E8E3E; padding: 4px 8px; border-radius: 4px; border: 1px solid #1E8E3E; font-weight: bold; font-size: 12px; }
    .badge-fail { background: #FCE8E6; color: #D93025; padding: 4px 8px; border-radius: 4px; border: 1px solid #D93025; font-weight: bold; font-size: 12px; }
    
    /* CARD STYLING */
    .css-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #E6E6E6; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. CACHING ---
@st.cache_resource
def get_rembg_session():
    return new_session("u2net") 

# --- 4. COMPLIANCE ENGINE (APPENDIX A & B) ---
def check_appendix_compliance(text, format_type):
    issues = []
    status = "PASS"
    
    # 1. Sustainability (Appendix B)
    suspicious_eco = ["sustainable", "green", "eco-friendly", "carbon", "planet"]
    if any(word in text.lower() for word in suspicious_eco):
        issues.append("❌ FAIL: 'Green' claims detected (Appendix B Violation).")
        status = "FAIL"

    # 2. Competitions (Appendix B)
    suspicious_comp = ["win", "competition", "prize", "enter now", "lucky"]
    if any(word in text.lower() for word in suspicious_comp):
        issues.append("❌ FAIL: Competition copy detected (Appendix B Violation).")
        status = "FAIL"
        
    # 3. Social Safe Zones (Appendix A)
    if format_type == "Instagram Story (9:16)":
        issues.append("ℹ️ INFO: Enforcing 200px/250px Safe Zones (Appendix A).")

    if not issues:
        issues.append("✅ ALL CHECKS PASSED: Brand Safe.")
        
    return status, issues

# --- 5. GENERATIVE ENGINE ---
def generate_creative(product_file, bg_prompt, text, platform, currency, price, session):
    # 1. Process Image
    input_img = Image.open(product_file).convert("RGBA")
    no_bg_product = remove(input_img, session=session)
    
    # 2. Canvas Dims
    dims = {
        "Instagram Post (1:1)": (1080, 1080),
        "Instagram Story (9:16)": (1080, 1920),
        "Web Banner (Landscape)": (1200, 628)
    }
    w, h = dims[platform]
    
    # 3. Contextual Background
    bg = Image.new('RGB', (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(bg)
    
    if "white" in bg_prompt.lower():
        pass
    elif "summer" in bg_prompt.lower():
        for y in range(h): # Blue gradient
            r = int(135 + (y/h)*120)
            g = int(206 + (y/h)*49)
            b = 250
            draw.line([(0, y), (w, y)], fill=(r,g,b))
    elif "kitchen" in bg_prompt.lower():
        draw.rectangle([(0, 0), (w, h)], fill="#F5F5DC")
        draw.rectangle([(0, h//2), (w, h)], fill="#D2B48C") 
    else:
        draw.rectangle([(0, 0), (w, h)], fill="#F4F7F9")

    # 4. Compose Product
    final_img = bg.convert("RGBA")
    
    prod_w, prod_h = no_bg_product.size
    if prod_h == 0: prod_h = 1
    scale = (h * 0.55) / prod_h
    new_size = (int(prod_w * scale), int(prod_h * scale))
    resized_prod = no_bg_product.resize(new_size)
    
    pos_x = (w - new_size[0]) // 2
    
    # Safe Zones (Appendix A)
    if platform == "Instagram Story (9:16)":
        safe_top = 200
        safe_bottom = h - 250
        available_h = safe_bottom - safe_top
        pos_y = safe_top + (available_h - new_size[1]) // 2
    else:
        pos_y = (h - new_size[1]) // 2
        
    final_img.paste(resized_prod, (pos_x, int(pos_y)), resized_prod)
    
    # 5. LOGO HANDLING
    logo_path = "logo.png" # Standard fallback
    # Try to find specific webp if available, else use standard logo
    if os.path.exists("Tesco-1.webp"):
        logo_path = "Tesco-1.webp"

    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_target_w = int(w * 0.25)
            aspect = logo.width / logo.height
            logo_target_h = int(logo_target_w / aspect)
            logo = logo.resize((logo_target_w, logo_target_h), Image.Resampling.LANCZOS)
            final_img.paste(logo, (w - logo_target_w - 40, 40), logo)
        except:
            draw.text((w-200, 50), "TESCO", fill="#00539F")
    else:
        # Fallback text if no logo file found
        draw.text((w-200, 50), "TESCO", fill="#00539F")
    
    # 6. CLUBCARD VALUE TILE (Dynamic Price)
    draw = ImageDraw.Draw(final_img)
    
    tile_w = 300
    tile_h = 220
    tile_x = w - tile_w - 40
    tile_y = h - tile_h - 40
    
    # White Box + Blue Border
    draw.rectangle([tile_x, tile_y, tile_x+tile_w, tile_y+tile_h], fill="white", outline="#00539F", width=5)
    
    # Red Header
    header_h = 60
    draw.rectangle([tile_x, tile_y, tile_x+tile_w, tile_y+header_h], fill="#EE1C2E")
    
    # Text
    try: font_head = ImageFont.truetype("arial.ttf", 30)
    except: font_head = ImageFont.load_default()
    draw.text((tile_x + 50, tile_y + 15), "Clubcard Price", fill="white", font=font_head)
    
    # Dynamic Price
    full_price = f"{currency}{price}"
    try: font_price = ImageFont.truetype("arial.ttf", 80)
    except: font_price = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), full_price, font=font_price)
    pw = bbox[2] - bbox[0]
    px = tile_x + (tile_w - pw) // 2
    py = tile_y + header_h + 30
    draw.text((px, py), full_price, fill="#00539F", font=font_price)

    # 7. Slogan
    if text:
        try: font_slogan = ImageFont.truetype("arial.ttf", 50)
        except: font_slogan = ImageFont.load_default()
        draw.text((50, h - 100), text, fill="#00539F", font=font_slogan)

    return final_img

# --- 6. SIDEBAR UI ---
with st.sidebar:
    if os.path.exists("Tesco-1.webp"):
        st.image("Tesco-1.webp", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='color:#EE1C2E'>TESCO</h1>", unsafe_allow_html=True)

    st.markdown("#### 🛠️ Campaign Settings") 
    platform = st.selectbox("Format", ["Instagram Post (1:1)", "Instagram Story (9:16)", "Web Banner (Landscape)"])
    
    st.markdown("#### 💰 Price Configuration") 
    c1, c2 = st.columns([1, 2])
    currency = c1.selectbox("Currency", ["£", "€", "$"])
    price_val = c2.text_input("Price", "15.00")
    
    st.markdown("#### 🎨 Creative Context") 
    bg_prompt = st.text_input("Background Style", "Summer Blue Sky")
    campaign_text = st.text_input("Slogan", "Great Value")

    st.divider()
    st.success("System Status: Online")

# --- 7. MAIN PAGE ---
st.markdown("""
<div style="padding:20px; border-left:6px solid #00539F; background:white; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px;">
    <h1 style="margin:0; font-size:2rem; color: #00539F;">Tesco AI Studio: Enterprise Edition</h1>
    <p style="color:#333; margin-top:5px; font-size: 16px;">
        Automated creative builder with <b>Appendix A/B Compliance</b> & Dynamic Pricing.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Product Images", type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if st.button(f"🚀 Generate Campaign for {len(uploaded_files)} Products"):
        session = get_rembg_session()
        st.write("")
        cols = st.columns(2)
        
        for i, file in enumerate(uploaded_files):
            with cols[i % 2]:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                
                # Check & Generate
                status, issues = check_appendix_compliance(campaign_text, platform)
                with st.spinner("Rendering..."):
                    final_img = generate_creative(file, bg_prompt, campaign_text, platform, currency, price_val, session)
                
                # Display
                st.image(final_img, use_container_width=True)
                
                # Compliance Report
                st.markdown("#### 🛡️ Compliance Report")
                if status == "PASS":
                    st.markdown(f'<span class="badge-pass">✅ PASS</span> <span style="color:#333">Ready for Distribution</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="badge-fail">❌ FAIL</span> <span style="color:#333">Blocked by Appendix B</span>', unsafe_allow_html=True)
                
                for issue in issues:
                    st.caption(issue)
                
                # Download
                if status == "PASS":
                    buf = io.BytesIO()
                    final_img.convert("RGB").save(buf, format="JPEG", quality=95)
                    st.download_button("⬇️ Download Asset", data=buf.getvalue(), file_name=f"TESCO_{i}.jpg", mime="image/jpeg", key=f"dl_{i}")
                
                st.markdown('</div>', unsafe_allow_html=True)
