import streamlit as st
import pickle
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="PhishGuard AI Pro", page_icon="🛡️", layout="wide")

# 2. Load the AI brain
try:
    model = pickle.load(open('phishing_model.pkl', 'rb'))
    tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
except FileNotFoundError:
    st.error("❌ Model files missing! Run 'model_builder.py' first.")
    st.stop()

# 3. Heuristic Engine (Layer 2 Defense)
def heuristic_check(text):
    score = 0
    reasons = []
    
    # Check for suspicious domains
    if "http" in text.lower():
        if any(ext in text.lower() for ext in [".net", ".xyz", ".bit", ".click"]):
            score += 30
            reasons.append("Non-official domain extension detected")
            
    # Check for brand spoofing
    brands = ["google", "netflix", "amazon", "microsoft", "paypal", "hr portal"]
    for brand in brands:
        if brand in text.lower() and f"{brand.replace(' ', '')}.com" not in text.lower().replace(" ", ""):
            score += 25
            reasons.append(f"Unofficial {brand.capitalize()} reference")

    # Check for pressure tactics
    urgency_words = ["4 hours", "immediately", "urgent", "final warning", "payroll freeze"]
    if any(word in text.lower() for word in urgency_words):
        score += 20
        reasons.append("High-pressure urgency detected")

    return score, reasons

# 4. Main Interface
st.title("🛡️ PhishGuard AI: Multi-Layered Threat Detection")
st.markdown("---")

# Sidebar for Navigation
option = st.sidebar.selectbox("Select Mode", ["Single Message Check", "Batch File Audit"])

if option == "Single Message Check":
    st.subheader("🔍 Real-Time Message Analysis")
    message = st.text_area("Paste message content here:", height=150)
    
    if st.button("🚀 Run Deep Analysis"):
        if message.strip():
            with st.spinner('Analyzing linguistic and metadata patterns...'):
                # AI Model Prediction
                data = tfidf.transform([message])
                prob = model.predict_proba(data)[0]
                ai_risk = prob[1] * 100
                
                # Heuristic Shield
                h_score, h_reasons = heuristic_check(message)
                
                # Combined Score
                final_risk = min(100, ai_risk + (h_score * 0.5))
                
                col1, col2 = st.columns(2)
                col1.metric("Final Risk Level", f"{final_risk:.1f}%")
                col2.metric("System Verdict", "🚨 PHISHING" if final_risk > 50 else "✅ SAFE")
                
                if final_risk > 50:
                    st.error(f"High Risk Alert! Risk Score: {final_risk:.1f}%")
                    with st.expander("🔍 View Risk Breakdown"):
                        st.write(f"**NLP Analysis:** AI detected phishing patterns with {ai_risk:.1f}% confidence.")
                        if h_reasons:
                            st.write("**Heuristic Red Flags:**")
                            for r in h_reasons:
                                st.write(f"- {r}")
                else:
                    st.success("Analysis Complete: Message appears legitimate.")
        else:
            st.warning("Please enter content to analyze.")

else:
    st.subheader("📊 Enterprise Batch Audit")
    st.write("Process large datasets to identify internal security threats.")
    
    uploaded_file = st.file_uploader("Upload CSV (Must have a 'message' column)", type="csv")
    
    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)
        
        if 'message' in df_upload.columns:
            if st.button("📈 Start Batch Audit"):
                with st.spinner('Auditing messages...'):
                    # Batch AI Processing
                    X_batch = tfidf.transform(df_upload['message'].astype(str))
                    df_upload['Risk Score %'] = model.predict_proba(X_batch)[:, 1] * 100
                    df_upload['Verdict'] = df_upload['Risk Score %'].apply(lambda x: '🚨 Phishing' if x > 50 else '✅ Safe')
                    
                    st.divider()
                    total = len(df_upload)
                    phish_count = len(df_upload[df_upload['Risk Score %'] > 50])
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Total Scanned", total)
                    c2.metric("Threats Detected", phish_count)
                    c3.metric("Safety Rating", f"{((total-phish_count)/total)*100:.1f}%")
                    
                    # Dashboard Visualization
                    st.bar_chart(df_upload['Verdict'].value_counts())
                    st.dataframe(df_upload[['message', 'Verdict', 'Risk Score %']].style.background_gradient(subset=['Risk Score %'], cmap='Reds'))
        else:
            st.error("Error: CSV must contain a 'message' column.")

st.sidebar.markdown("---")
st.sidebar.caption("PhishGuard AI v2.0 | Security Audit Mode")