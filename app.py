import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="SMS Spam Classifier",
    page_icon="📩",
    layout="centered"
)

# ------------------------------
# Custom CSS for UI Styling
# ------------------------------
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 16px;
            margin-bottom: 30px;
            color: #dcdcdc;
        }
        .stTextArea textarea {
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #ff7a18;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        .result-box {
            text-align: center;
            padding: 20px;
            border-radius: 12px;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Load Model & Vectorizer
# ------------------------------
@st.cache_resource
def load_models():
    tfidf = pickle.load(open('Datasets/vectorizer.pkl', 'rb'))
    model = pickle.load(open('Datasets/model.pkl', 'rb'))
    return tfidf, model


tfidf, model = load_models()

# ------------------------------
# Text Preprocessing Function
# ------------------------------
ps = PorterStemmer()

@st.cache_data
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    # Remove non-alphanumeric
    text = [word for word in text if word.isalnum()]

    # Remove stopwords & punctuation
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]

    # Stemming
    text = [ps.stem(word) for word in text]

    return " ".join(text)

# ------------------------------
# UI Layout
# ------------------------------

st.markdown('<div class="title">📩 SMS Spam Classifier</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect whether a message is Spam or Not using Machine Learning</div>', unsafe_allow_html=True)

# Input Box
input_msg = st.text_area("✉️ Enter your message here:", height=150, placeholder="Type your SMS message...")

# Button
if st.button("🚀 Classify Message"):

    if input_msg.strip() == "":
        st.warning("⚠️ Please enter a message first.")
    else:
        # Processing animation
        with st.spinner("Analyzing message..."):
            transformed_text = transform_text(input_msg)
            vectorized_text = tfidf.transform([transformed_text])
            result = model.predict(vectorized_text)[0]

        # Result Display
        if result == 0:
            st.markdown(
                '<div class="result-box" style="background-color:#28a745;">✅ Not Spam Message</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="result-box" style="background-color:#dc3545;">🚨 Spam Message Detected</div>',
                unsafe_allow_html=True
            )

# ------------------------------
# Footer
# ------------------------------
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 14px;'>
        Built with ❤️ using Streamlit | ML Powered Spam Detection
    </div>
""", unsafe_allow_html=True)
