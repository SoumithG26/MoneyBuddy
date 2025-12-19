import streamlit as st
import requests
import json
import os

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(page_title="SmartPocket 💰", layout="centered")

# ---------------------------------
# Persistent Storage Setup
# ---------------------------------
USER_DIR = "users"
os.makedirs(USER_DIR, exist_ok=True)

def load_user_data(username):
    path = f"{USER_DIR}/{username}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_user_data(username):
    data = dict(st.session_state)
    data.pop("username", None)
    path = f"{USER_DIR}/{username}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------------------
# Featherless AI Setup
# ---------------------------------
API_URL = "https://router.huggingface.co/featherless-ai/v1/completions"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}",
    "Content-Type": "application/json"
}

def query_ai(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "meta-llama/Llama-3.1-8B-Instruct",
                "prompt": prompt,
                "max_tokens": 80,
                "temperature": 0.4,
                "top_p": 0.8,
                "stop": [
                    "\n\n",
                    "You're",
                    "You are",
                    "Keep",
                    "I'm so",
                    "What do you",
                    "Do you want"
                ]
            },
            timeout=30
        )

        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["text"].strip()
        elif "error" in data:
            return f"⚠️ AI Error: {data['error']['message']}"
        else:
            return "⚠️ Unexpected AI response."

    except Exception as e:
        return f"⚠️ AI connection failed."

# ---------------------------------
# Login (Basic Authentication)
# ---------------------------------
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    st.title("🔐 SmartPocket Login")
    username = st.text_input("Enter your name (no password)")

    if st.button("Continue") and username.strip():
        st.session_state.username = username.strip().lower()
        user_data = load_user_data(st.session_state.username)
        if user_data:
            st.session_state.update(user_data)
        else:
            st.session_state.initialized = False
            st.session_state.chat_history = []
        st.rerun()

    st.stop()

# ---------------------------------
# App Title
# ---------------------------------
st.title("💰 SmartPocket")
st.caption(f"Welcome, {st.session_state.username.capitalize()}")

# ---------------------------------
# Initialize Session State
# ---------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------
# Parent Budget Setup
# ---------------------------------
if not st.session_state.initialized:
    st.header("👨‍👩‍👧 Parent Budget Setup")

    total_budget = st.number_input("Total Budget (₹)", min_value=1, step=10)
    total_days = st.number_input("Number of Days", min_value=1, step=1)

    if st.button("Start Budget"):
        st.session_state.total_budget = float(total_budget)
        st.session_state.remaining_budget = float(total_budget)
        st.session_state.total_days = int(total_days)
        st.session_state.remaining_days = int(total_days)
        st.session_state.daily_allowance = total_budget / total_days
        st.session_state.initialized = True
        save_user_data(st.session_state.username)
        st.rerun()

# ---------------------------------
# Main Dashboard
# ---------------------------------
else:
    st.header("📊 Budget Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Remaining Budget", f"₹{st.session_state.remaining_budget:.2f}")
    col2.metric("Remaining Days", st.session_state.remaining_days)
    col3.metric("Today's Allowance", f"₹{st.session_state.daily_allowance:.2f}")

    st.divider()

    # ---------------------------------
    # Expense Entry (Once per day logic optional)
    # ---------------------------------
    st.subheader("🛒 Log Today's Expense")

    expense = st.number_input("Expense Amount (₹)", min_value=0.0, step=1.0)
    description = st.text_input("Expense Description")

    if st.button("Add Expense"):
        if st.session_state.remaining_days <= 0:
            st.warning("No days remaining!")
        else:
            st.session_state.remaining_budget -= expense
            st.session_state.remaining_days -= 1

            if st.session_state.remaining_days > 0:
                st.session_state.daily_allowance = (
                    st.session_state.remaining_budget /
                    st.session_state.remaining_days
                )
            else:
                st.session_state.daily_allowance = 0

            save_user_data(st.session_state.username)
            st.success("Expense saved!")
            st.rerun()

    st.divider()

    # ---------------------------------
    # AI Chatbot
    # ---------------------------------
    st.subheader("🤖 Smart Spending Assistant")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask me before spending...")

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        prompt = (
            "You are a friendly money guide talking to a child.\n\n"
            "STRICT RULES:\n"
            "- Reply in at most 3 short sentences\n"
            "- Give one clear suggestion\n"
            "- Do not repeat yourself\n"
            "- Do not overpraise\n"
            "- Do not explain your reasoning\n\n"
            f"Remaining budget: ₹{st.session_state.remaining_budget:.2f}\n"
            f"Remaining days: {st.session_state.remaining_days}\n"
            f"Daily allowance: ₹{st.session_state.daily_allowance:.2f}\n\n"
            f"Child says: {user_input}\n\n"
            "Reply directly:"
        )

        ai_reply = query_ai(prompt)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        save_user_data(st.session_state.username)

        with st.chat_message("assistant"):
            st.markdown(ai_reply)

    st.divider()

    # ---------------------------------
    # Logout & Reset
    # ---------------------------------
    colA, colB = st.columns(2)

    with colA:
        if st.button("🚪 Logout"):
            save_user_data(st.session_state.username)
            st.session_state.clear()
            st.rerun()

    with colB:
        if st.button("🔄 Reset Budget"):
            st.session_state.initialized = False
            st.session_state.chat_history = []
            save_user_data(st.session_state.username)
            st.rerun()
