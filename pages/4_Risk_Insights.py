"""
Risk Insights page - provides recommendations and risk analysis
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_and_clean_data
from utils.metrics import calculate_risk_metrics, calculate_financial_impact

# Configure page
st.set_page_config(page_title="Risk Insights", page_icon="🎯", layout="wide")

st.title("🎯 Risk Insights & Recommendations")
st.markdown("Data-driven recommendations to reduce fraud risk")

# Load data
@st.cache_data
def load_data():
    return load_and_clean_data('data/creditcard.csv')

df = load_data()
risk_metrics = calculate_risk_metrics(df)
impact = calculate_financial_impact(df)

# Risk metrics cards
st.subheader("📊 Key Risk Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📈 Fraud vs Normal Ratio",
        f"{risk_metrics['fraud_to_normal_ratio']:.1f}x"
    )

with col2:
    if risk_metrics['busiest_fraud_hour'] is not None:
        st.metric(
            "⏰ Riskiest Hour",
            f"{risk_metrics['busiest_fraud_hour']:02d}:00"
        )
    else:
        st.metric("⏰ Riskiest Hour", "No data")

with col3:
    st.metric(
        "💸 Total Fraud Loss",
        f"${impact['total_fraud_loss']:,.0f}"
    )

# Risk matrix by category
st.subheader("🎯 Risk Matrix by Amount Category")

# Create risk matrix
categories = ['Small (< $100)', 'Medium ($100-$500)', 'Large ($500-$1000)', 'Very Large (> $1000)']
normal_counts = []
fraud_counts = []

for i, cat in enumerate(categories):
    if i == 0:
        normal_counts.append(len(df[(df['Class']==0) & (df['Amount']<100)]))
        fraud_counts.append(len(df[(df['Class']==1) & (df['Amount']<100)]))
    elif i == 1:
        normal_counts.append(len(df[(df['Class']==0) & (df['Amount']>=100) & (df['Amount']<500)]))
        fraud_counts.append(len(df[(df['Class']==1) & (df['Amount']>=100) & (df['Amount']<500)]))
    elif i == 2:
        normal_counts.append(len(df[(df['Class']==0) & (df['Amount']>=500) & (df['Amount']<1000)]))
        fraud_counts.append(len(df[(df['Class']==1) & (df['Amount']>=500) & (df['Amount']<1000)]))
    else:
        normal_counts.append(len(df[(df['Class']==0) & (df['Amount']>=1000)]))
        fraud_counts.append(len(df[(df['Class']==1) & (df['Amount']>=1000)]))

risk_matrix = pd.DataFrame({
    'Category': categories,
    'Normal Count': normal_counts,
    'Fraud Count': fraud_counts
})

# Calculate risk percentage
risk_matrix['Risk Rate (%)'] = (risk_matrix['Fraud Count'] / (risk_matrix['Normal Count'] + risk_matrix['Fraud Count'])) * 100
risk_matrix['Risk Rate (%)'] = risk_matrix['Risk Rate (%)'].fillna(0).round(4)

st.dataframe(risk_matrix, use_container_width=True, hide_index=True)

# Recommendations tabs
st.subheader("💡 Recommendations")

tab1, tab2, tab3 = st.tabs(["🚨 Immediate Actions", "📋 Short-term Actions", "🎯 Strategic Actions"])

with tab1:
    st.markdown("""
    ### ⚡ Immediate Actions (This Week)
    
    1. **Monitor Large Transactions** (> $1000)
       - Manual review for transactions > $5000
       - Send real-time alerts to customers
    
    2. **Increase Monitoring During Risky Hours**
       - Add more reviewers between 12 AM - 4 AM
       - Enable additional verification during these hours
    
    3. **Flag Unusual Patterns**
       - Transactions that deviate from customer history
       - Multiple transactions in short time period
    """)

with tab2:
    st.markdown("""
    ### 📅 Short-term Actions (Next Month)
    
    1. **Build Early Detection System**
       - Train ML model on historical data
       - Integrate with real-time transaction system
    
    2. **Train Review Team**
       - Workshops on new fraud patterns
       - Share successful case studies
    
    3. **Update Risk Rules**
       - Adjust thresholds based on findings
       - Add new fraud indicators
    """)

with tab3:
    st.markdown("""
    ### 🎯 Strategic Actions (3-6 Months)
    
    1. **Real-time Fraud Detection**
       - Reduce detection time from hours to seconds
       - Implement behavioral analysis
    
    2. **Advanced Analytics**
       - Build customer behavior profiles
       - Automatic anomaly detection
    
    3. **Industry Collaboration**
       - Share fraud patterns with other institutions
       - Participate in fraud prevention networks
    """)

# Risk summary
st.subheader("📋 Executive Risk Summary")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Estimated Annual Savings",
        f"${impact['total_fraud_loss'] * 0.3:,.0f}",
        help="30% reduction target"
    )

with col2:
    st.metric(
        "ROI Timeline",
        "3-6 months",
        help="Expected return on investment"
    )