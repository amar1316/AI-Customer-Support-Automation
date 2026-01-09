import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import streamlit as st
from tickets.pending_store import get_pending, remove_pending
from tickets.ticket_manager import log_ticket

st.set_page_config(page_title="AI Support Dashboard", layout="wide")

st.title("🧠 AI Customer Support – Approval Panel")

pending = get_pending()

if not pending:
    st.success("No pending tickets 🎉")
else:
    for i, ticket in enumerate(pending):
        with st.expander(f"Ticket #{i+1} | {ticket['intent']}"):
            st.write("**Customer Message:**")
            st.write(ticket["message"])

            st.write("**AI Suggested Reply:**")
            edited_reply = st.text_area(
                "Edit reply before sending",
                ticket["suggested_reply"],
                key=i
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Approve & Send", key=f"approve_{i}"):
                    log_ticket(
                        ticket["message"],
                        ticket["intent"],
                        ticket["confidence"],
                        "HUMAN APPROVED"
                    )
                    remove_pending(i)
                    st.rerun()


            with col2:
                if st.button("❌ Reject", key=f"reject_{i}"):
                    log_ticket(
                        ticket["message"],
                        ticket["intent"],
                        ticket["confidence"],
                        "HUMAN REJECTED"
                    )
                    remove_pending(i)
                    st.rerun()

