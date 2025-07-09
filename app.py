import streamlit as st
import re
import string
import pickle
import pandas as pd

# === CONFIG ===
st.set_page_config(page_title="Mood to Meal", page_icon="🍱", layout="centered")

# === CUSTOM CSS ===
st.markdown("""
    <style>
    /* === BACKGROUND & BASE APP === */
    .stApp {
        background: url("https://images.unsplash.com/photo-1600891964599-f61ba0e24092") no-repeat center center fixed;
        background-size: cover;
        font-family: 'Segoe UI', sans-serif;
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.2);
        color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* === TEXT === */
    html, body, [class*="css"] {
        color: #ffffff;
        text-align: center;
    }

    /* === TEXT AREA === */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1);
        color: black;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 10px;
        padding: 1rem;
        backdrop-filter: blur(8px);
    }

    /* === BUTTON === */
    .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(6px);
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.4);
        color: #000;
    }

    /* === CONTAINER === */
    .block-container {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 30px rgba(0,0,0,0.1);
    }

    .element-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(6px);
    }

    /* === ANIMASI === */
    .food-card {
        animation: slideIn 1s ease-in-out;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# === SIDEBAR CONTENT ===
st.sidebar.markdown("""
### 👥 Kelompok 4
Pengantar Kecerdasan Buatan

- (2308561015) - I Made Aditya  
- (2308561027) - KM. Mutia Tri Ayu Santi  
- (2308561033) - I Gusti Riyani Astarani  
- (2308561039) - Kadek Intan Dheya Pratiwi  
- (2308561081) - Christian Valentino  
- (2308561117) - Made Ananta Adnyana
""")

# === LOAD MODEL ===
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model_naivebayes_best.pkl', 'rb') as f:
    model = pickle.load(f)

# === TEXT PROCESSING ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def simple_tokenize(text):
    return text.split()

stopwords = set([
    'yang','untuk','pada','dari','dan','di','ke','itu','ini','dengan','juga','sudah','karena',
    'seperti','ada','saja','akan','dalam','tidak','lebih','bisa','atau','jadi','agar','kalau',
    'hanya','saat','masih','mereka','kita','saya','aku','kamu','dia','kami','mu','lah','pun',
    'nya','kok','loh','dong'
])

def simple_stemmer(word):
    for prefix in ['ber','ter','me','mem','men','meng','di','ke','se']:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in ['kan','an','i','nya']:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
    return word

def preprocess(text):
    cleaned = clean_text(text)
    tokens = simple_tokenize(cleaned)
    filtered = [t for t in tokens if t not in stopwords]
    stemmed = [simple_stemmer(w) for w in filtered]
    return ' '.join(stemmed)

# === MOOD MAPPING ===
mood_to_food = {
    'anger': ['Pizza keju', 'Es teh lemon', 'Salad segar'],
    'fear': ['Teh hangat', 'Roti cokelat', 'Susu jahe'],
    'happy': ['Kue tart', 'Es krim stroberi', 'Smoothie buah'],
    'love': ['Cokelat panas', 'Pasta creamy', 'Kopi susu'],
    'sadness': ['Sop ayam', 'Bubur hangat', 'Cokelat manis']
}

mood_emoji = {
    'anger': '😠',
    'fear': '😨',
    'happy': '😄',
    'love': '😍',
    'sadness': '😢'
}

mood_quotes = {
    'anger': "Tarik napas dalam-dalam, tenangkan hatimu.",
    'fear': "Rasa takut adalah tanda bahwa kamu peduli.",
    'happy': "Senang itu menular, teruskan semangatmu!",
    'love': "Cinta adalah kekuatan luar biasa.",
    'sadness': "Tidak apa-apa merasa sedih, kamu tidak sendiri."
}

# === SESSION HISTORY ===
if 'history' not in st.session_state:
    st.session_state['history'] = []

# === MAIN INTERFACE ===
st.title("🍱 MOOD TO MEAL")
st.markdown("Masukkan perasaan atau curhatan kamu hari ini, dan biar AI bantu carikan makanan yang cocok!")

user_input = st.text_area("🧠 Bagaimana perasaanmu hari ini?", height=150)
submit = st.button("🎯 Rekomendasikan")

if submit and user_input.strip():
    processed = preprocess(user_input)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    proba = model.predict_proba(vectorized)[0]
    labels = model.classes_

    st.session_state['history'].append((user_input, prediction))

    st.markdown(f"<h1 style='text-align:center;'>{mood_emoji.get(prediction)}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>Mood kamu: {prediction.upper()}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-style:italic;'>{mood_quotes.get(prediction)}</p>", unsafe_allow_html=True)

    st.markdown("### 🍽️ Rekomendasi makanan:")
    for food in mood_to_food[prediction]:
        st.markdown(f"- {food}")

    st.markdown("### 📊 Keyakinan Model (Probabilitas)")
    df_proba = pd.DataFrame({
        "Mood": labels,
        "Probabilitas (%)": [round(p * 100, 2) for p in proba]
    }).sort_values("Probabilitas (%)")
    st.bar_chart(df_proba.set_index("Mood"))

if st.session_state['history']:
    st.markdown("### 🕘 Riwayat Curhat:")
    for text, mood in reversed(st.session_state['history']):
        st.markdown(f"- 🗣️ _{text}_ → **{mood.upper()}**")
