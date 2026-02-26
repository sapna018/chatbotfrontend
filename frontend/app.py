import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Titanic Glass AI Dashboard",
    page_icon="🚢",
    layout="wide"
)

# ---------------- GLASSMORPHISM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Glass container */
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* KPI cards */
.kpi-card {
    text-align: center;
}

/* Chat bubbles */
.user-bubble {
    background: rgba(0, 119, 255, 0.6);
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 8px;
}

.bot-bubble {
    background: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>🚢 Titanic Glass AI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-Powered Maritime Analytics</p>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
csv_path = os.path.join(os.path.dirname(__file__), "Titanic-Dataset.csv")
df = pd.read_csv(csv_path)

# ---------------- KPI SECTION ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="glass kpi-card"><h3>Total Passengers</h3><h2>{len(df)}</h2></div>',
        unsafe_allow_html=True
    )

with col2:
    survival_rate = round(df["Survived"].mean() * 100, 2)
    st.markdown(
        f'<div class="glass kpi-card"><h3>Survival Rate</h3><h2>{survival_rate}%</h2></div>',
        unsafe_allow_html=True
    )

with col3:
    avg_age = round(df["Age"].mean(), 1)
    st.markdown(
        f'<div class="glass kpi-card"><h3>Average Age</h3><h2>{avg_age}</h2></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------- LAYOUT SPLIT ----------------
chat_col, chart_col = st.columns([1, 1.2])

# ---------------- CHAT SECTION ----------------
with chat_col:
    st.markdown('<div class="glass"><h3>💬 AI Assistant</h3></div>', unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Clear Chat Button
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    # Chat Input
    user_input = st.chat_input("Ask about Titanic passengers...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                "https://web-production-3fc9.up.railway.app/ask",
                json={"query": user_input}
            )
            answer = response.json()["answer"]
        except:
            answer = "⚠️ Backend not running!"

        # Typing effect
        typing_container = st.empty()
        typed_text = ""

        typing_container.markdown(
            '<div class="bot-bubble">🤖 AI is typing...</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.5)

        for char in answer:
            typed_text += char
            typing_container.markdown(
                f'<div class="bot-bubble">🤖 {typed_text}</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.01)

        typing_container.empty()

        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-bubble">🧑 {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-bubble">🤖 {msg["content"]}</div>',
                unsafe_allow_html=True
            )

# ---------------- CHART SECTION ----------------
with chart_col:
    st.markdown('<div class="glass"><h3>📊 Live Analytics</h3></div>', unsafe_allow_html=True)

    chart_type = st.selectbox(
        "Choose Visualization",
        ["Survival by Gender", "Passenger Class Distribution", "Age Distribution"]
    )

    fig, ax = plt.subplots()

    if chart_type == "Survival by Gender":
        sns.barplot(x="Sex", y="Survived", data=df, ax=ax)

    elif chart_type == "Passenger Class Distribution":
        sns.countplot(x="Pclass", data=df, ax=ax)

    elif chart_type == "Age Distribution":
        sns.histplot(df["Age"].dropna(), kde=True, ax=ax)

    st.pyplot(fig)  
