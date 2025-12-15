import streamlit as st
import re
import string
import pickle
import pandas as pd
from datetime import datetime

# === CONFIG ===
st.set_page_config(
    page_title="Mood to Meal | AI-Powered Emotion Analysis", 
    page_icon="🍱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === DARK PROFESSIONAL CSS ===
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');
    
    /* === BACKGROUND === */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* === MAIN CONTAINER === */
    .main .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1400px;
    }
    
    /* === HERO SECTION === */
    .hero-section {
        background: linear-gradient(135deg, #e94560 0%, #0f3460 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(233, 69, 96, 0.3);
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #ffffff;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        color: white;
        font-weight: 600;
        margin-top: 0.8rem;
    }
    
    /* === CARD === */
    .dark-card {
        background: #1e2a3a;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin: 1rem 0;
        border: 1px solid rgba(233, 69, 96, 0.2);
    }
    
    /* === SECTION HEADERS === */
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* === TEXT AREA === */
    .stTextArea textarea {
        background: #0f1419 !important;
        color: #ffffff !important;
        border: 2px solid #e94560 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #e94560 !important;
        box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #7c8a99 !important;
    }
    
    .stTextArea label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* === BUTTON === */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #c72845 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(233, 69, 96, 0.4) !important;
        width: 100% !important;
        margin-top: 1rem !important;
        font-family: 'Poppins', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 28px rgba(233, 69, 96, 0.5) !important;
    }
    
    /* === MOOD RESULT === */
    .mood-result {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(233, 69, 96, 0.15) 0%, rgba(15, 52, 96, 0.15) 100%);
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 2px solid rgba(233, 69, 96, 0.3);
    }
    
    .mood-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
    }
    
    .mood-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #e94560;
        margin: 0.5rem 0;
        text-shadow: 0 2px 8px rgba(233, 69, 96, 0.3);
    }
    
    .mood-quote {
        font-size: 1.1rem;
        color: #b8c5d6;
        font-style: italic;
        margin: 1rem auto;
        max-width: 600px;
        line-height: 1.6;
    }
    
    /* === FOOD ITEMS === */
    .food-item {
        background: #0f1419;
        padding: 1rem 1.5rem;
        margin: 0.6rem 0;
        border-radius: 12px;
        border-left: 4px solid #e94560;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        font-size: 1.05rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .food-item:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 16px rgba(233, 69, 96, 0.3);
        border-left-color: #ff6b6b;
    }
    
    /* === INFO ITEMS === */
    .info-item {
        padding: 0.9rem 0;
        border-bottom: 1px solid rgba(233, 69, 96, 0.2);
        color: #b8c5d6;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    
    .info-item:last-child {
        border-bottom: none;
    }
    
    .info-item strong {
        color: #ffffff;
        font-size: 1rem;
    }
    
    .info-icon {
        display: inline-block;
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* === HISTORY === */
    .history-item {
        background: #0f1419;
        padding: 1rem 1.5rem;
        margin: 0.6rem 0;
        border-radius: 12px;
        border-left: 4px solid #e94560;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        font-size: 0.95rem;
        color: #b8c5d6;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        transform: translateX(8px);
        background: #1a2332;
    }
    
    .history-item strong {
        color: #ffffff;
    }
    
    /* === CHART STYLING === */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #e94560 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b8c5d6 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #4ecca3 !important;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        margin-top: 3rem;
        color: #7c8a99;
        font-size: 0.9rem;
        border-top: 1px solid rgba(233, 69, 96, 0.2);
    }
    
    .footer-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #e94560;
        margin-bottom: 0.5rem;
    }
    
    /* === COLUMNS === */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* === HIDE STREAMLIT BRANDING === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* === FIX TEXT VISIBILITY === */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, span, div {
        color: #b8c5d6;
    }
    
    /* === SPINNER === */
    .stSpinner > div {
        border-top-color: #e94560 !important;
    }
    </style>
""", unsafe_allow_html=True)

# === LOAD MODEL ===
try:
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('model_naivebayes_best.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("⚠️ Model files not found. Please ensure 'tfidf_vectorizer.pkl' and 'model_naivebayes_best.pkl' are in the same directory.")
    st.stop()

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
    'anger': ['🍕 Spicy Margherita Pizza', '🍋 Iced Lemon Tea', '🥗 Fresh Garden Salad', '🌶️ Chili Con Carne'],
    'fear': ['☕ Chamomile Tea', '🍞 Warm Chocolate Croissant', '🥛 Honey Ginger Milk', '🫖 Lavender Earl Grey'],
    'happy': ['🎂 Strawberry Shortcake', '🍦 Vanilla Bean Gelato', '🥤 Tropical Smoothie Bowl', '🍰 Tiramisu'],
    'love': ['🍫 Belgian Hot Chocolate', '🍝 Creamy Carbonara Pasta', '☕ Caramel Macchiato', '🥐 Almond Croissant'],
    'sadness': ['🍲 Chicken Noodle Soup', '🥣 Comfort Porridge', '🍫 Dark Chocolate Brownie', '🍵 Warm Green Tea']
}

mood_emoji = {
    'anger': '😠',
    'fear': '😨',
    'happy': '😄',
    'love': '😍',
    'sadness': '😢'
}

mood_quotes = {
    'anger': "Take a deep breath. Channel this energy into something powerful.",
    'fear': "Courage is not the absence of fear, but the triumph over it.",
    'happy': "Your joy is contagious. Keep spreading that beautiful energy!",
    'love': "Love is the bridge between hearts. Cherish this moment.",
    'sadness': "It's okay to feel this way. Healing begins with acceptance."
}

mood_colors = {
    'anger': '#e74c3c',
    'fear': '#f39c12',
    'happy': '#2ecc71',
    'love': '#e91e63',
    'sadness': '#3498db'
}

# === SESSION STATE ===
if 'history' not in st.session_state:
    st.session_state['history'] = []

# === HERO SECTION ===
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🍱 Mood to Meal</h1>
        <p class="hero-subtitle">AI-Powered Emotional Intelligence & Personalized Food Recommendations</p>
        <span class="hero-badge">✨ Powered by Machine Learning</span>
    </div>
""", unsafe_allow_html=True)

# === MAIN INTERFACE ===
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💭 Share Your Emotions</div>', unsafe_allow_html=True)
    user_input = st.text_area(
        "How are you feeling today?",
        height=200,
        placeholder="Express yourself freely... Tell me about your day, your thoughts, your emotions...",
        label_visibility="collapsed"
    )
    submit = st.button("🔮 Analyze My Mood & Get Recommendations")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">ℹ️ How It Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-item"><span class="info-icon">🧠</span><strong>AI Emotion Detection</strong><br/>Advanced NLP analyzes your text</div>
    <div class="info-item"><span class="info-icon">🍽️</span><strong>Smart Food Matching</strong><br/>Personalized comfort food suggestions</div>
    <div class="info-item"><span class="info-icon">📊</span><strong>Confidence Analysis</strong><br/>Detailed probability breakdown</div>
    <div class="info-item"><span class="info-icon">📝</span><strong>Journey Tracking</strong><br/>Monitor your emotional patterns</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === PREDICTION LOGIC ===
if submit and user_input.strip():
    with st.spinner('🤖 Analyzing your emotions with AI...'):
        try:
            processed = preprocess(user_input)
            vectorized = vectorizer.transform([processed])
            prediction = model.predict(vectorized)[0]
            proba = model.predict_proba(vectorized)[0]
            labels = model.classes_

            # Store in history with timestamp
            st.session_state['history'].append({
                'text': user_input,
                'mood': prediction,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            # === RESULT DISPLAY ===
            st.markdown('<div class="mood-result">', unsafe_allow_html=True)
            st.markdown(f'<div class="mood-emoji">{mood_emoji.get(prediction)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mood-title">Your Mood: {prediction.upper()}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mood-quote">"{mood_quotes.get(prediction)}"</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # === FOOD RECOMMENDATIONS & CHART ===
            col_food, col_chart = st.columns([1, 1], gap="medium")
            
            with col_food:
                st.markdown('<div class="dark-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🍽️ Personalized Comfort Foods</div>', unsafe_allow_html=True)
                for food in mood_to_food[prediction]:
                    st.markdown(f'<div class="food-item">{food}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_chart:
                st.markdown('<div class="dark-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">📊 Confidence Distribution</div>', unsafe_allow_html=True)
                
                # Create DataFrame for chart
                df_proba = pd.DataFrame({
                    "Mood": labels,
                    "Confidence": [p * 100 for p in proba]
                }).sort_values("Confidence", ascending=False)
                
                # Display chart
                st.bar_chart(df_proba.set_index("Mood"), height=250, color="#e94560")
                
                # Show top prediction
                st.metric(
                    label="Top Prediction",
                    value=f"{prediction.upper()}",
                    delta=f"{max(proba)*100:.1f}% confidence"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"⚠️ An error occurred during analysis: {str(e)}")

# === HISTORY SECTION ===
if st.session_state['history']:
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📝 Your Emotional Journey</div>', unsafe_allow_html=True)
    
    for i, entry in enumerate(reversed(st.session_state['history'][-5:])):
        mood_color = mood_colors.get(entry['mood'], '#e94560')
        st.markdown(
            f'<div class="history-item">'
            f'<strong style="color: #ffffff;">#{len(st.session_state["history"]) - i}</strong> | '
            f'{mood_emoji.get(entry["mood"])} '
            f'<em>{entry["text"][:70]}{"..." if len(entry["text"]) > 70 else ""}</em><br/>'
            f'<small style="color: #7c8a99;">{entry["timestamp"]}</small> → '
            f'<strong style="color: {mood_color}">{entry["mood"].upper()}</strong>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
    <div class="footer">
        <div class="footer-title">Mood to Meal</div>
        <p>Powered by Natural Language Processing & Machine Learning</p>
        <p style="margin-top: 0.5rem; font-size: 0.85rem;">
            Built with Python • Streamlit • Scikit-learn • 
        </p>
    </div>
""", unsafe_allow_html=True)



# import streamlit as st
# import re
# import string
# import pickle
# import pandas as pd

# # === CONFIG ===
# st.set_page_config(page_title="Mood to Meal", page_icon="🍱", layout="centered")

# # === CUSTOM CSS ===
# st.markdown("""
#     <style>
#     /* === BACKGROUND & BASE APP === */
#     .stApp {
#         background: url("https://images.unsplash.com/photo-1600891964599-f61ba0e24092") no-repeat center center fixed;
#         background-size: cover;
#         font-family: 'Segoe UI', sans-serif;
#     }

#     /* === SIDEBAR === */
#     section[data-testid="stSidebar"] {
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(10px);
#         border-right: 1px solid rgba(255,255,255,0.2);
#         color: white !important;
#     }
#     [data-testid="stSidebar"] * {
#         color: white !important;
#     }

#     /* === TEXT === */
#     html, body, [class*="css"] {
#         color: #ffffff;
#         text-align: center;
#     }

#     /* === TEXT AREA === */
#     .stTextArea textarea {
#         background: rgba(255, 255, 255, 0.1);
#         color: black;
#         border: 1px solid rgba(255,255,255,0.3);
#         border-radius: 10px;
#         padding: 1rem;
#         backdrop-filter: blur(8px);
#     }

#     /* === BUTTON === */
#     .stButton > button {
#         background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(6px);
#         border: none;
#         color: white;
#         font-weight: bold;
#         border-radius: 10px;
#         padding: 0.5rem 1.5rem;
#         transition: all 0.3s ease-in-out;
#     }
#     .stButton > button:hover {
#         background: rgba(255, 255, 255, 0.4);
#         color: #000;
#     }

#     /* === CONTAINER === */
#     .block-container {
#         background: rgba(255, 255, 255, 0.15);
#         border-radius: 20px;
#         padding: 2rem;
#         margin-top: 2rem;
#         backdrop-filter: blur(12px);
#         box-shadow: 0 4px 30px rgba(0,0,0,0.1);
#     }

#     .element-container {
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 15px;
#         padding: 1rem;
#         backdrop-filter: blur(6px);
#     }

#     /* === ANIMASI === */
#     .food-card {
#         animation: slideIn 1s ease-in-out;
#     }

#     @keyframes slideIn {
#         from { opacity: 0; transform: translateY(30px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
#     </style>
# """, unsafe_allow_html=True)

# # === SIDEBAR CONTENT ===
# st.sidebar.markdown("""
# ### 👥 Kelompok 4
# Pengantar Kecerdasan Buatan

# - (2308561015) - I Made Aditya  
# - (2308561027) - KM. Mutia Tri Ayu Santi  
# - (2308561033) - I Gusti Riyani Astarani  
# - (2308561039) - Kadek Intan Dheya Pratiwi  
# - (2308561081) - Christian Valentino  
# - (2308561117) - Made Ananta Adnyana
# """)

# # === LOAD MODEL ===
# with open('tfidf_vectorizer.pkl', 'rb') as f:
#     vectorizer = pickle.load(f)

# with open('model_naivebayes_best.pkl', 'rb') as f:
#     model = pickle.load(f)

# # === TEXT PROCESSING ===
# def clean_text(text):
#     text = text.lower()
#     text = re.sub(r'\d+', '', text)
#     text = text.translate(str.maketrans('', '', string.punctuation))
#     return text.strip()

# def simple_tokenize(text):
#     return text.split()

# stopwords = set([
#     'yang','untuk','pada','dari','dan','di','ke','itu','ini','dengan','juga','sudah','karena',
#     'seperti','ada','saja','akan','dalam','tidak','lebih','bisa','atau','jadi','agar','kalau',
#     'hanya','saat','masih','mereka','kita','saya','aku','kamu','dia','kami','mu','lah','pun',
#     'nya','kok','loh','dong'
# ])

# def simple_stemmer(word):
#     for prefix in ['ber','ter','me','mem','men','meng','di','ke','se']:
#         if word.startswith(prefix):
#             word = word[len(prefix):]
#             break
#     for suffix in ['kan','an','i','nya']:
#         if word.endswith(suffix):
#             word = word[:-len(suffix)]
#             break
#     return word

# def preprocess(text):
#     cleaned = clean_text(text)
#     tokens = simple_tokenize(cleaned)
#     filtered = [t for t in tokens if t not in stopwords]
#     stemmed = [simple_stemmer(w) for w in filtered]
#     return ' '.join(stemmed)

# # === MOOD MAPPING ===
# mood_to_food = {
#     'anger': ['Pizza keju', 'Es teh lemon', 'Salad segar'],
#     'fear': ['Teh hangat', 'Roti cokelat', 'Susu jahe'],
#     'happy': ['Kue tart', 'Es krim stroberi', 'Smoothie buah'],
#     'love': ['Cokelat panas', 'Pasta creamy', 'Kopi susu'],
#     'sadness': ['Sop ayam', 'Bubur hangat', 'Cokelat manis']
# }

# mood_emoji = {
#     'anger': '😠',
#     'fear': '😨',
#     'happy': '😄',
#     'love': '😍',
#     'sadness': '😢'
# }

# mood_quotes = {
#     'anger': "Tarik napas dalam-dalam, tenangkan hatimu.",
#     'fear': "Rasa takut adalah tanda bahwa kamu peduli.",
#     'happy': "Senang itu menular, teruskan semangatmu!",
#     'love': "Cinta adalah kekuatan luar biasa.",
#     'sadness': "Tidak apa-apa merasa sedih, kamu tidak sendiri."
# }

# # === SESSION HISTORY ===
# if 'history' not in st.session_state:
#     st.session_state['history'] = []

# # === MAIN INTERFACE ===
# st.title("🍱 MOOD TO MEAL")
# st.markdown("Masukkan perasaan atau curhatan kamu hari ini, dan biar AI bantu carikan makanan yang cocok!")

# user_input = st.text_area("🧠 Bagaimana perasaanmu hari ini?", height=150)
# submit = st.button("🎯 Rekomendasikan")

# if submit and user_input.strip():
#     processed = preprocess(user_input)
#     vectorized = vectorizer.transform([processed])
#     prediction = model.predict(vectorized)[0]
#     proba = model.predict_proba(vectorized)[0]
#     labels = model.classes_

#     st.session_state['history'].append((user_input, prediction))

#     st.markdown(f"<h1 style='text-align:center;'>{mood_emoji.get(prediction)}</h1>", unsafe_allow_html=True)
#     st.markdown(f"<h2 style='text-align:center;'>Mood kamu: {prediction.upper()}</h2>", unsafe_allow_html=True)
#     st.markdown(f"<p style='text-align:center; font-style:italic;'>{mood_quotes.get(prediction)}</p>", unsafe_allow_html=True)

#     st.markdown("### 🍽️ Rekomendasi makanan:")
#     for food in mood_to_food[prediction]:
#         st.markdown(f"- {food}")

#     st.markdown("### 📊 Keyakinan Model (Probabilitas)")
#     df_proba = pd.DataFrame({
#         "Mood": labels,
#         "Probabilitas (%)": [round(p * 100, 2) for p in proba]
#     }).sort_values("Probabilitas (%)")
#     st.bar_chart(df_proba.set_index("Mood"))

# if st.session_state['history']:
#     st.markdown("### 🕘 Riwayat Curhat:")
#     for text, mood in reversed(st.session_state['history']):
#         st.markdown(f"- 🗣️ _{text}_ → **{mood.upper()}**")
