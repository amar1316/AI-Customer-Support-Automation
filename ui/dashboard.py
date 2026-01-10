import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Support Admin Panel", layout="wide")
st.title("🧠 AI Customer Support – Admin Panel")

# =========================
# PENDING TICKETS
# =========================
st.header("⏳ Pending Tickets")

try:
    pending_resp = requests.get(f"{API_BASE}/pending", timeout=5)
    pending = pending_resp.json()

    if not pending:
        st.success("No pending tickets 🎉")
    else:
        for i, ticket in enumerate(pending):
            with st.expander(f"Ticket #{i+1} | Intent: {ticket['intent']}"):
                st.markdown("### 📩 Customer Message")
                st.write(ticket["message"])

                st.markdown("### 🤖 AI Suggested Reply (Editable)")
                edited_reply = st.text_area(
                    "Edit reply before approval",
                    ticket["suggested_reply"],
                    key=f"reply_{i}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✅ Approve", key=f"approve_{i}"):
                        requests.post(
                            f"{API_BASE}/approve/{i}",
                            json={"final_reply": edited_reply}
                        )
                        st.success("Ticket approved and logged")
                        st.rerun()

                with col2:
                    if st.button("❌ Reject", key=f"reject_{i}"):
                        requests.post(f"{API_BASE}/reject/{i}")
                        st.warning("Ticket rejected and logged")
                        st.rerun()

except Exception as e:
    st.error(f"Pending API error: {e}")

# =========================
# AUDIT LOGS WITH FILTERS
# =========================
st.divider()
st.header("📊 Audit Logs")

if st.button("🔄 Refresh Logs"):
    st.rerun()

try:
    logs_resp = requests.get(f"{API_BASE}/logs", timeout=5)
    logs = logs_resp.json()

    if not logs:
        st.info("No audit logs yet.")
    else:
        df = pd.DataFrame(logs)

        # ---- FILTER CONTROLS ----
        st.subheader("🔍 Filters")

        col1, col2, col3 = st.columns(3)

        with col1:
            action_filter = st.multiselect(
                "Filter by Action",
                options=sorted(df["action"].unique()),
                default=sorted(df["action"].unique())
            )

        with col2:
            intent_filter = st.multiselect(
                "Filter by Intent",
                options=sorted(df["intent"].unique()),
                default=sorted(df["intent"].unique())
            )

        with col3:
            search_text = st.text_input(
                "Search in Customer Message",
                placeholder="refund, billing, error..."
            )

        # ---- APPLY FILTERS ----
        filtered_df = df[
            df["action"].isin(action_filter) &
            df["intent"].isin(intent_filter)
        ]

        if search_text:
            filtered_df = filtered_df[
                filtered_df["message"].str.contains(search_text, case=False, na=False)
            ]

        # Show newest first
        filtered_df = filtered_df[::-1]

        # ---- DISPLAY ----
        st.subheader("📄 Filtered Audit Logs")
        st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Logs API error: {e}")

