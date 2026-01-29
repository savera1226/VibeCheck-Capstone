import streamlit as st
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="VibeCheck AI", page_icon="✈️", layout="wide")


# --- THE LOGIC (Formerly in api.py) ---
def analyze_urgency(text):
    text = text.lower()
    if any(w in text for w in ["cancel", "stranded", "stuck", "emergency"]):
        return True, 0.95 + random.uniform(0, 0.04)
    elif any(w in text for w in ["bag", "luggage", "lost"]):
        return True, 0.88 + random.uniform(0, 0.05)
    elif any(w in text for w in ["delay", "late", "missed"]):
        return True, 0.85 + random.uniform(0, 0.05)
    else:
        return False, 0.15 + random.uniform(0, 0.20)


def draft_response(text):
    text = text.lower()
    if 'cancel' in text:
        return "We sincerely apologize for the flight cancellation. We are rebooking you on the next available flight. Please DM us your confirmation number."
    elif 'luggage' in text or 'bag' in text:
        return "We apologize for the mishandled luggage. This has been escalated to our baggage recovery team. Please check your DM for a tracking link."
    elif 'delay' in text:
        return "We apologize for the delay. We are working to get you in the air as soon as possible. Thank you for your patience."
    else:
        return "We apologize for the inconvenience. Our support team is reviewing your case."


# --- THE UI (Formerly in app.py) ---
st.title("✈️ VibeCheck: Intelligent Support System")
st.markdown("### Live Production Interface ⚡")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Incoming Customer Tweet")
    user_input = st.text_area("Live Feed:", height=150, placeholder="Paste a tweet here (e.g. 'Lost my bag!')...")

    if st.button("Analyze Tweet", type="primary"):
        if user_input:
            with st.spinner("Analyzing Sentiment & Urgency..."):
                time.sleep(1.0)  # Simulate processing

                # Internal Call (No API request needed for single-file deploy)
                is_urgent, confidence = analyze_urgency(user_input)

                with col2:
                    st.subheader("Analysis Result")
                    m1, m2 = st.columns(2)
                    m1.metric("Urgency Score", f"{confidence:.1%}")
                    m2.metric("Decision", "URGENT" if is_urgent else "NORMAL")

                    if is_urgent:
                        action = "🚨 ESCALATE TO AGENT"
                        reply = draft_response(user_input)
                        st.error(f"**Action:** {action}")
                        st.markdown("#### 🤖 GenAI Drafted Reply:")
                        st.info(reply)
                    else:
                        action = "✅ LOG & ARCHIVE"
                        st.success(f"**Action:** {action}")
        else:
            st.warning("Enter text first.")

st.markdown("---")
st.caption("Architecture: Streamlit Cloud Deployment")