
# 📡 Gemini Historical Artifact Description App

Generate rich, AI-powered descriptions for any historical artifact!  
Upload an image, specify your prompt and word count, and get a custom, engaging artifact description powered by Google Gemini.


---
## ✨ Features

- **Modern, Responsive UI:** Clean two-column layout with a bright, attractive palette.
- **Image Upload:** Enhance your prompt with artifact images (JPG, JPEG, PNG).
- **Custom Word Count:** Choose the length of your generated description.
- **Google Gemini Integration:** Uses Gemini AI for high-quality, context-aware text generation.
- **Copy to Clipboard:** Easily copy generated descriptions for your research or documentation.

---

## 🚀 Getting Started

### 1. Clone the Repository
```sh
git clone https://github.com/syam-bukkuru/Gemini-Historical-Artifact-Description-App.git
cd Gemini-Historical-Artifact-Description-App
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed.
```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_MODEL=gemini-pro
```

### 4. Run the App
```sh
streamlit run app.py
```

---

## 🖼️ Usage

1. Enter a prompt describing your artifact (e.g., "Tutankhamun's Golden Mask").
2. Select your desired word count.
3. (Optional) Upload an image of the artifact.
4. Click **Generate Artifact Description**.
5. View and copy your custom description from the results panel.

---

## 📦 Project Structure

```
.
├── app.py
├── requirements.txt
├── .env.example
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
└── README.md
```

---

## 🙏 Acknowledgements

- [Google Gemini API](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [Pillow (PIL)](https://python-pillow.org/)

---
