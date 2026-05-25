# app.py

import streamlit as st
import pickle

from database import conn, cursor

# =========================
# LOAD TRAINED MODEL
# =========================

model = pickle.load(
    open("models/model.pkl", "rb")
)

vectorizer = pickle.load(
    open("models/vectorizer.pkl", "rb")
)

df = pickle.load(
    open("models/data.pkl", "rb")
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="CareerAI",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0E1117;
    color: white;
}

.big-font {
    font-size: 55px !important;
    font-weight: bold;
    color: #00ADB5;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #B0B0B0;
    margin-bottom: 40px;
}

.card {
    background: linear-gradient(
        135deg,
        #1E1E1E,
        #23263A
    );
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
    border-left: 6px solid #00ADB5;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.01);
}

.card h2 {
    color: #00ADB5;
    margin-bottom: 10px;
}

.card h3 {
    color: white;
}

.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 12px;
    height: 55px;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border: none;
    margin-top: 20px;
}

.stButton>button:hover {
    background-color: #008C94;
    color: white;
}

.stTextInput input {
    border-radius: 10px;
}

textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.markdown(
    '<p class="big-font">🚀 CareerAI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">AI-Powered Career Recommendation System</p>',
    unsafe_allow_html=True
)

# =========================
# INPUT SECTION
# =========================

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "👤 Name"
    )

    education = st.selectbox(
        "🎓 Education",
        [
            "ECE",
            "CSE",
            "IT",
            "EEE",
            "Mechanical"
        ]
    )

    domains = st.text_input(
        "🌐 Preferred Domains",
        placeholder="AI, Cloud, IoT, Cyber Security"
    )

with col2:
    skills = st.text_area(
        "🛠 Skills",
        placeholder="Python, Machine Learning, SQL"
    )

    interests = st.text_area(
        "❤️ Interests",
        placeholder="Data Science, Robotics"
    )

# =========================
# BUTTON
# =========================

if st.button(
    "✨ Generate Career Recommendation"
):

    # =========================
    # VALIDATION
    # =========================

    if skills == "" or interests == "":
        st.error(
            "⚠ Please enter skills and interests"
        )

    else:
        # =========================
        # USER INPUT
        # =========================

        user_input = (
            skills + " " +
            interests + " " +
            domains + " " +
            education
        )

        # =========================
        # VECTORIZE INPUT
        # =========================

        user_vector = vectorizer.transform(
            [user_input]
        )

        # =========================
        # GET RECOMMENDATIONS
        # =========================

        distances, indices = model.kneighbors(
            user_vector
        )

        # =========================
        # HEADER
        # =========================

        st.markdown(
            "## 🎯 Top Career Recommendations"
        )

        shown = []

        # =========================
        # LOOP RESULTS
        # =========================

        for idx, i in enumerate(indices[0]):

            career = df.iloc[i][
                "Recommended_Career"
            ]

            # REMOVE DUPLICATES

            if career not in shown:
                shown.append(career)

                # =========================
                # MATCH SCORE
                # =========================

                score = float(
                    round(
                        (1 - distances[0][idx]) * 100,
                        2
                    )
                )

                # =========================
                # CARD UI (Fixed Indentation Here)
                # =========================

                st.markdown(
                    f"""
<div class="card">
    <h2>🚀 {career}</h2>
    <h3>🔥 Match Score: {score}%</h3>
</div>
""",
                    unsafe_allow_html=True
                )

                # =========================
                # SAVE TO DATABASE
                # =========================

                cursor.execute(
                    """
                    INSERT INTO users
                    (
                        name,
                        education,
                        skills,
                        interests,
                        domains,
                        recommended_career,
                        match_score
                    )
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        name,
                        education,
                        skills,
                        interests,
                        domains,
                        career,
                        score
                    )
                )

        # =========================
        # COMMIT DATABASE
        # =========================

        conn.commit()

        st.success(
            "✅ Recommendations Saved Successfully!"
        )