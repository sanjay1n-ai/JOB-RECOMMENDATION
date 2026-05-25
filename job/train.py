# train.py

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("dataset/AI-based Career Recommendation System.csv")

# =========================
# CHECK COLUMN NAMES
# =========================

print(df.columns)

# Example expected columns:
# Skills, Interests, Career

# =========================
# HANDLE MISSING VALUES
# =========================

df.fillna("", inplace=True)

# =========================
# CREATE COMBINED TEXT
# =========================

df["combined"] = (
    df["Skills"] + " " +
    df["Interests"]
)

# =========================
# CONVERT TEXT TO VECTORS
# =========================

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["combined"])

# =========================
# TRAIN MODEL
# =========================

model = NearestNeighbors(
    n_neighbors=5,
    metric='cosine'
)

model.fit(X)

# =========================
# SAVE MODEL
# =========================

pickle.dump(model, open("models/model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))
pickle.dump(df, open("models/data.pkl", "wb"))

print("Model trained and saved successfully!")