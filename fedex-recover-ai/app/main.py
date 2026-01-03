import sys
import os
import streamlit as st
import pandas as pd
import joblib

# Setup system path for internal modules
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from pipeline.orchestrator import ai_decision_engine

st.set_page_config(
    page_title="FedEx Recover-AI",
    page_icon="📦",
    layout="wide"
)

# UI Header
st.title("📦 FedEx Recover-AI")
st.caption("Intelligent Debt Collection Agency (DCA) Orchestration Platform")

# Persistence Layer: Load Serialized Model
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error("System Error: model.pkl not found. Please initialize the training pipeline.")
    st.stop()

# Operational KPIs
st.header("Strategic Overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Portfolio", "1,250", "3.2%")
m2.metric("Projected Recovery", "$2.4M", "11%")
m3.metric("Avg. Agency SLA", "22h", "-2h")
m4.metric("AI Precision", "91.4%", "Stable")

st.divider()

# Case Analysis Engine
st.header("Case Assessment & AI Allocation")
left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("Account Parameters")
    amount = st.number_input("Invoice Value ($)", min_value=0, value=5000)
    days_overdue = st.slider("Ageing (Days)", 1, 365, 45)
    history_score = st.slider("Internal Credit Score", 0, 100, 75)

    predict_btn = st.button("Generate AI Recommendation", use_container_width=True)

with right_col:
    if predict_btn:
        # Prepare feature vector for inference
        features = pd.DataFrame(
            [[amount, days_overdue, history_score]], 
            columns=["amount", "days_overdue", "past_history_score"]
        )
        
        prob = model.predict_proba(features)[0][1]
        score = prob * 100

        # Execute Business Logic via Orchestrator
        decision = ai_decision_engine(score, amount, days_overdue)

        # Output Results
        st.subheader(f"Recovery Propensity: {score:.1f}%")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.info(f"**Assigned Agency:** {decision['agency']}")
            st.info(f"**Target SLA:** {decision['sla_hours']} Hours")
        with res_col2:
            st.info(f"**Case Priority:** {decision['priority']}")
            st.info(f"**Risk Profile:** {decision['risk_level']}")
        
        st.success(f"**Suggested Strategy:** {decision['action']}")

st.divider()

# Governance & Audit Trail
st.header("Agency Performance & Audit Trail")
sample_logs = pd.DataFrame({
    "Timestamp": ["2026-01-02 10:00", "2026-01-02 11:30", "2026-01-02 14:15"],
    "Entity": ["Agency Alpha", "System Bot", "Agency Beta"],
    "Action": ["Case Accepted", "Auto-Escalation", "Payment Scheduled"],
    "Status": ["Active", "Alert", "Pending Verification"]
})
st.table(sample_logs)