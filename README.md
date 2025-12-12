# Tesco AI Studio: The 'Guardian' Creative Engine 🛍️✨

**Winner/Entry for the Retail Media Creative Tool Hackathon** *Autonomy with Guardrails for Enterprise Retail Media.*

---

## 📖 Project Overview
**Tesco AI Studio** is an enterprise-grade Generative AI platform designed to solve the "Compliance vs. Creativity" bottleneck in retail media. 

Currently, producing campaign assets requires manual resizing for diverse formats (Instagram, Web, In-store) and strict adherence to complex brand guidelines (Appendix A & B). Small errors—like using banned "competition" terms or violating safe zones—can lead to rejection loops and legal risks.

**Our Solution:** A self-serve creative studio that empowers advertisers to generate professional assets in seconds, with a built-in **'Guardian Engine'** that enforces Tesco's strict compliance rules *before* a file can be downloaded.

---

## 🚀 Key Features

### 1. 🎨 Generative Creative Suite
* **Smart Ingestion:** Instantly removes backgrounds from raw packshots using U2Net (`rembg`).
* **Context Awareness:** Generates brand-aligned backgrounds (e.g., "Summer Garden," "Modern Kitchen") based on text prompts.
* **Brand Palettes:** Applies approved Tesco color schemes automatically.

### 2. 🛡️ The 'Guardian' Compliance Engine
A rule-based logic layer that strictly enforces Hackathon Specs:
* **Appendix B Enforcement:** Automatically detects and blocks "Hard Fail" terms like *"Sustainability," "Competitions,"* and *"Price in Slogan."*
* **Alcohol Safety:** Detects alcohol products and flags mandatory **Drinkaware** checks.
* **Design Compliance:** Enforces **Appendix A** rules, including 200px/250px safe zones for Instagram Stories.

### 3. 📏 Multi-Format & Dynamic Design
* **One-Click Resizing:** Generates 1:1 (Post), 9:16 (Story), and Landscape (Banner) formats instantly.
* **Dynamic Value Tiles:** Users input a price, and the system renders the official **Clubcard Value Tile** (Red header, White body, Tesco Blue border) pixel-perfectly.
* **Optimization:** Auto-compresses all assets to **<500KB** for web performance.

---

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **Image Processing:** [Pillow (PIL)](https://python-pillow.org/)
* **AI Background Removal:** [rembg](https://github.com/danielgatis/rembg) (U2Net Model)
* **Logic:** Custom Python Compliance Rules Engine

---

## 📸 Screenshots

| **1. The Creative Studio** | **2. The 'Guardian' (Fail State)** |
|:---:|:---:|
| ![Success Demo](path/to/your/success_screenshot.png) | ![Fail Demo](path/to/your/fail_screenshot.png) |
| *Generates compliant assets with dynamic Price Tiles.* | *Blocks "Win a Prize" claims immediately.* |

*(Note: Replace the paths above with your actual screenshot URLs if hosting images, or drag-and-drop images into your GitHub README editor.)*

---

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/tesco-ai-studio.git](https://github.com/yourusername/tesco-ai-studio.git)
    cd tesco-ai-studio
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

4.  **Access the Dashboard**
    Open your browser and navigate to `http://localhost:8501`.

---

## 📂 Project Structure
tesco-ai-studio/ ├── app.py # Main application logic ├── requirements.txt # Python dependencies ├── Tesco-1.webp # Official logo asset └── README.md # Documentation

---

## 🏆 Hackathon Alignment
This project directly addresses the challenge of **"Empowering advertisers while ensuring compliance."** * **Scalability:** Batch processing handles entire catalogs in one go.
* **Safety:** The hard-coded ruleset ensures no non-compliant asset ever leaves the system.
* **Efficiency:** Reduces asset production time from hours to seconds.

---

*Built with ❤️ for the Retail Media Creative Tool Hackathon.*
