import streamlit as st
import requests

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="SmartPocket 💰",
    layout="centered"
)

st.title("💰 SmartPocket")
st.caption("Learn smart spending & saving with AI guidance")

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
                "inputs": prompt,
                "max_tokens": 300,
                "temperature": 0.7,
            },
            timeout=30
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["text"].strip()
        elif "error" in data:
            return f"⚠️ AI Error: {data['error']}"
        else:
            return "⚠️ Unexpected AI response."

    except Exception as e:
        return f"⚠️ AI connection failed: {str(e)}"

# ---------------------------------
# Session State Initialization
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

    total_budget = st.number_input(
        "Total Budget (₹)",
        min_value=1,
        step=10
    )

    total_days = st.number_input(
        "Number of Days",
        min_value=1,
        step=1
    )

    if st.button("Start Budget"):
        st.session_state.total_budget = float(total_budget)
        st.session_state.remaining_budget = float(total_budget)
        st.session_state.total_days = int(total_days)
        st.session_state.remaining_days = int(total_days)
        st.session_state.daily_allowance = total_budget / total_days
        st.session_state.initialized = True
        st.rerun()

# ---------------------------------
# Main App (Child View)
# ---------------------------------
else:
    st.header("📊 Budget Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Remaining Budget", f"₹{st.session_state.remaining_budget:.2f}")
    col2.metric("Remaining Days", st.session_state.remaining_days)
    col3.metric("Today's Allowance", f"₹{st.session_state.daily_allowance:.2f}")

    st.divider()

    # ---------------------------------
    # Expense Entry
    # ---------------------------------
    st.subheader("🛒 Log Today's Expense")

    expense = st.number_input(
        "Expense Amount (₹)",
        min_value=0.0,
        step=1.0
    )

    description = st.text_input(
        "Expense Description",
        placeholder="Snacks, toy, game, etc."
    )

    if st.button("Add Expense"):
        if st.session_state.remaining_days <= 0:
            st.warning("No days remaining!")
        else:
            st.session_state.remaining_budget -= expense
            st.session_state.remaining_days -= 1

            if st.session_state.remaining_days > 0:
                st.session_state.daily_allowance = (
                    st.session_state.remaining_budget
                    / st.session_state.remaining_days
                )
            else:
                st.session_state.daily_allowance = 0

            st.success("Expense recorded!")
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

        with st.chat_message("user"):
            st.markdown(user_input)

        prompt = f"""
You are a friendly financial assistant for a child.

Rules:
- Use simple and kind language
- Encourage balance (not overspending or oversaving)
- Suggest saving plans when needed
- Explain consequences gently

Current budget:
Remaining budget: ₹{st.session_state.remaining_budget:.2f}
Remaining days: {st.session_state.remaining_days}
Daily allowance: ₹{st.session_state.daily_allowance:.2f}

Child's question:
{user_input}

Give helpful advice:
"""

        ai_reply = query_ai(prompt)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        with st.chat_message("assistant"):
            st.markdown(ai_reply)

    st.divider()

    # ---------------------------------
    # Reset
    # ---------------------------------
    if st.button("🔄 Reset Budget"):
        st.session_state.clear()
        st.rerun()
