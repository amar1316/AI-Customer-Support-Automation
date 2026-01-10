import streamlit as st
import requests

API_BASE = "https://ai-customer-support-automation-2.onrender.com"  # change this

st.set_page_config(page_title="AI Support Approval Panel", layout="wide")
st.title("🧠 AI Customer Support – Human Approval Panel")

response = requests.get(f"{API_BASE}/pending")

if response.status_code != 200:
    st.error("Failed to fetch pending tickets")
    st.stop()

pending = response.json()

if not pending:
    st.success("No pending tickets 🎉")
else:
    for i, ticket in enumerate(pending):
        with st.expander(f"Ticket #{i+1} | Intent: {ticket['intent']}"):
            st.write("### 📩 Customer Message")
            st.write(ticket["message"])

            st.write("### 🤖 AI Suggested Reply")
            st.text_area(
                "Suggested reply",
                ticket["suggested_reply"],
                key=f"reply_{i}",
                disabled=True
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Approve", key=f"approve_{i}"):
                    requests.post(f"{API_BASE}/approve/{i}")
                    st.rerun()

            with col2:
                if st.button("❌ Reject", key=f"reject_{i}"):
                    requests.post(f"{API_BASE}/reject/{i}")
                    st.rerun()
