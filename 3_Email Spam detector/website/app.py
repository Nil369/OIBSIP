import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

st.set_page_config(
    page_title="Email Spam Classifier",  # Set the title of the web page
    page_icon="img/logo.png",  # Set the logo of the web page (use a valid image path)
)

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load the TF-IDF vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Custom CSS to style the UI
st.markdown("""
    <style>
        .stButton>button {
            background-color: #0A79DF;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 3px 10px 3px 10px;
            border:none;
        }
        .stButton>button:hover {
            background-color:#007BFF ;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 3px 10px 3px 10px;
            border:none;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<h1 style="color:#74B9FF;">Email Spam Classifier</h1>""",unsafe_allow_html=True)

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    # 1. Preprocess
    transformed_sms = transform_text(input_sms)
    # 2. Vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. Predict
    result = model.predict(vector_input)[0]
    # 4. Display results with custom colors and images
    if result == 1:
        st.markdown("""<h2 style="color:#FF3E4D">Spam</h2>""", unsafe_allow_html=True)
        st.image("./img/spam.webp", width=300)  # Make sure to add your image in the correct path
    elif result == " ":
        st.markdown("<h2>Can't Claasify Blank Values<br/><span>Please Enter a valid Message</span></h2>", unsafe_allow_html=True)
    else:
        st.markdown("""<h2 style="color:#45CE30">Not Spam</h2>""", unsafe_allow_html=True)
        st.image("./img/ham.png", width=300)  # Make sure to add your image in the correct path
