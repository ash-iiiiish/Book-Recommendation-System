import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/kumar/OneDrive/Desktop/TRY-2/Tasks-Submission/Assignment20/data.csv")
    df["text"] = (
        df["title"].fillna("") + " " +
        df["authors"].fillna("") + " " +
        df["categories"].fillna("") + " " +
        df["description"].fillna("")
    )

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        tokens = [w for w in text.split() if w not in ENGLISH_STOP_WORDS]
        return " ".join(tokens)

    df["clean_text"] = df["text"].apply(clean_text)
    return df

df = load_data()

tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
tfidf_matrix = tfidf.fit_transform(df["clean_text"])
cosine_sim = cosine_similarity(tfidf_matrix)

def recommend(book, top_n=5):
    idx = df[df["title"] == book].index[0]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [df.iloc[i[0]]["title"] for i in scores[1:top_n+1]]

st.title("📚 Book Recommendation System")

book_selected = st.selectbox("Select a Book", df["title"].values)

if st.button("Get Recommendations"):
    recommendations = recommend(book_selected)
    st.subheader("Recommended Books")
    for book in recommendations:
        st.write("•", book)
