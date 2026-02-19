import os
import random
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image

load_dotenv()

# --------------------------
# Historical Facts
# --------------------------

HISTORICAL_FACTS = [
    "The Library of Alexandria was one of the largest libraries of the ancient world.",
    "The Rosetta Stone was key to deciphering Egyptian hieroglyphs.",
    "The Terracotta Army includes thousands of life-sized figures buried with Qin Shi Huang.",
    "The city of Pompeii was preserved by volcanic ash from Mount Vesuvius in 79 CE.",
    "The Antikythera mechanism is an ancient Greek device for predicting astronomical positions.",
]

# --------------------------
# Prompt Builder
# --------------------------

def build_prompt(topic: str, word_count: int) -> str:
    return (
        "You are a careful historian writing for a general audience. "
        "Write an informative and engaging historical description about the following topic. "
        "Emphasize verified context, provenance, and cultural significance. "
        "Avoid speculation; if a detail is uncertain, state that it is uncertain. "
        "Use clear prose and avoid bullet points. "
        f"Target length: exactly {word_count} words.\n\n"
        f"Topic: {topic}\n"
    )

# --------------------------
# Image Setup
# --------------------------

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
    return None

# --------------------------
# Gemini API Call
# --------------------------

def get_gemini_response(input_text, image_data, prompt, api_key):
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
    model = genai.GenerativeModel(model_name)

    if image_data:
        response = model.generate_content([input_text, image_data[0], prompt])
    else:
        response = model.generate_content([input_text, prompt])

    return response.text

# --------------------------
# Main App
# --------------------------

def main():
    st.set_page_config(
        page_title="Gemini Historical Artifact Description App",
        page_icon="📡",
        layout="wide"
    )

    st.markdown("""
    <style>
    body, .stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    color: #e2e8f0 !important;
}

/* MAIN TITLE */
.artifact-title {
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #c7d2fe !important;
    font-family: 'Playfair Display', serif;
    margin-bottom: 0.5rem;
}

/* SUBTITLE */
.artifact-sub {
    font-size: 1.2rem !important;
    color: #cbd5e1 !important;
    margin-bottom: 2rem;
}

/* SECTION TITLE */
.artifact-output-title {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #c084fc !important;
    margin-bottom: 1rem;
}

/* OUTPUT TEXT */
.artifact-output-text {
    font-size: 1.1rem !important;
    line-height: 1.7;
    color: #e2e8f0 !important;
}



/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%) !important;
    box-shadow: 0 4px 20px #7c3aed44 !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #a78bfa 0%, #7c3aed 100%) !important;
    box-shadow: 0 8px 30px #7c3aed66 !important;
}

/* INPUT TEXT SIZE */
textarea, input {
    font-size: 1rem !important;
}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="artifact-title"> 📡 Gemini Historical Artifact Description App</div>', unsafe_allow_html=True)
    st.markdown('<div class="artifact-sub">Generate rich, AI-powered descriptions for any historical artifact. Upload an image and specify your prompt and word count for a custom result.</div>', unsafe_allow_html=True)

    api_key = os.getenv("GEMINI_API_KEY")

    col1, col2 = st.columns([1.1, 1.2], gap="large")

    # Input Section (Left)
    with col1:
        with st.container():
            st.markdown('<div class="artifact-card">', unsafe_allow_html=True)
            st.markdown('<label class="input-label">Input Prompt</label>', unsafe_allow_html=True)
            input_text = st.text_area(
                label="Input Prompt",
                placeholder="Describe any artifact, e.g., 'Tutankhamun's Golden Mask'",
                key="input_prompt",
                height=90,
                help="Enter the name or description of any artifact.",
                label_visibility="collapsed"
            )
            st.markdown('<label class="input-label">Desired Word Count</label>', unsafe_allow_html=True)
            word_count = st.slider(
                label="Desired Word Count",
                min_value=50,
                max_value=2000,
                value=250,
                step=50,
                key="word_count_slider",
                help="Choose the length of the generated description.",
                label_visibility="collapsed"
            )
            st.markdown('<label class="input-label">Choose an image of an artifact...</label>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                label="Choose an image of an artifact...",
                type=["jpg", "jpeg", "png"],
                key="artifact_image",
                help="Upload an image to enhance the description.",
                label_visibility="collapsed"    
            )
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", width=320)
            st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
            submit = st.button("🚀 Generate Artifact Description", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Output Section (Right)
    with col2:
        with st.container():
            st.markdown('<div class="artifact-card artifact-output-card">', unsafe_allow_html=True)
            st.markdown('<div class="artifact-output-title">Results</div>', unsafe_allow_html=True)
            if submit:
                if not api_key:
                    st.error("Google Gemini API Key is missing in .env file.")
                elif not input_text.strip():
                    st.error("Input prompt is required.")
                else:
                    try:
                        with st.spinner("Generating description..."):
                            image_data = input_image_setup(uploaded_file)
                            input_prompt = build_prompt(input_text, word_count)
                            response = get_gemini_response(input_text, image_data, input_prompt, api_key)
                        st.markdown(f'<div class="artifact-output-text" id="artifact-output">{response}</div>', unsafe_allow_html=True)
                        st.caption(f"Word count: {len(response.split())}")
                        st.markdown(
                            f'<button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById(\'artifact-output\').innerText)">Copy to Clipboard</button>',
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error(f"⚠️ Error: {str(e)}")
            else:
                st.markdown('<div class="artifact-output-text" style="color:#aaa;">The generated artifact description will appear here.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()