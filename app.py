
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from src.detector import predict_url, predict_message

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Phishing & Online Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CUSTOM STYLE ----------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("🛡️ Phishing & Online Fraud Detection System")

st.markdown(
    "An intelligent machine learning system for detecting "
    "potentially phishing URLs and suspicious messages."
)

st.divider()

# ---------------- HELPER FUNCTION ----------------

def save_result(category, input_text, result, risk):
    st.session_state.history.append({
        "Date & Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Category": category,
        "Input": input_text,
        "Prediction": result,
        "Risk Score (%)": risk
    })


def show_result(result, risk):
    if result == "Phishing":
        st.error(f"🚨 Phishing Detected | Risk Score: {risk}%")

    elif result in ["Fraud", "Fraudulent / Spam"]:
        st.error(f"🚨 Suspicious Message Detected | Risk Score: {risk}%")

    else:
        st.success(f"✅ No threat detected by the model | Risk Score: {risk}%")

    st.progress(min(max(int(risk), 0), 100))

    st.caption(
        "Risk score represents the model's estimated score, "
        "not a verified probability or security guarantee."
    )


# ---------------- NAVIGATION ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "🌐 URL Scanner",
    "💬 Message Scanner",
    "📜 Detection History"
])

# ---------------- DASHBOARD ----------------

with tab1:

    st.subheader("Detection Overview")

    history = pd.DataFrame(st.session_state.history)

    total = len(history)

    if total > 0:
        threats = history["Prediction"].isin(
            ["Phishing", "Fraud", "Fraudulent / Spam"]
        ).sum()
        safe = total - threats
    else:
        threats = 0
        safe = 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Scans", total)
    col2.metric("Threats Detected", threats)
    col3.metric("No Threat Detected", safe)

    st.divider()

    st.subheader("Recent Activity")

    if total > 0:
        st.dataframe(
            history.tail(10).iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No scans yet. Start by scanning a URL or message.")

    st.caption("Statistics are based on scans in this active session.")


# ---------------- URL SCANNER ----------------

with tab2:

    st.subheader("Website Phishing Detection")

    st.write("Enter a website URL to check for potential phishing.")

    url = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        key="url_input"
    )

    if st.button("🔍 Scan URL", use_container_width=True):

        if not url.strip():
            st.warning("Please enter a URL.")

        else:
            try:
                with st.spinner("Analyzing URL..."):

                    output = predict_url(url)

                result = output["result"]
                risk = output["risk_score"]

                show_result(result, risk)

                save_result(
                    "URL",
                    url,
                    result,
                    risk
                )

            except Exception as e:
                st.error(f"URL scanning error: {e}")


# ---------------- MESSAGE SCANNER ----------------

with tab3:

    st.subheader("Suspicious Message Detection")

    st.write(
        "Paste an SMS, email message, or suspicious text "
        "to check its classification."
    )

    message = st.text_area(
        "Enter your message",
        placeholder="Paste your message here...",
        height=150
    )

    if st.button("🔍 Scan Message", use_container_width=True):

        if not message.strip():
            st.warning("Please enter a message.")

        else:
            try:
                with st.spinner("Analyzing message..."):

                    output = predict_message(message)

                result = output["result"]
                risk = output["risk_score"]

                show_result(result, risk)

                save_result(
                    "Message",
                    message,
                    result,
                    risk
                )

            except Exception as e:
                st.error(f"Message scanning error: {e}")


# ---------------- DETECTION HISTORY ----------------

with tab4:

    st.subheader("Previous Detection Records")

    history = pd.DataFrame(st.session_state.history)

    if not history.empty:

        st.dataframe(
            history.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download History as CSV",
            data=csv,
            file_name="detection_history.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info("No detection records available yet.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Machine Learning-Based Phishing and Online Fraud Detection System | "
    "Python • Scikit-learn • TF-IDF • Logistic Regression • Streamlit"
)
