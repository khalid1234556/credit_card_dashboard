"""
Executive Overview page - shows high-level KPIs for management
"""
import streamlit as st
from utils.data_loader import load_and_clean_data, get_basic_stats
from utils.metrics import calculate_financial_impact
from utils.charts import create_fraud_timeline, create_amount_distribution

# Configure page
st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

# Page title
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50;'>
    💳 Executive Overview - Credit Card Fraud Risk
    </h1>
    <hr>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = load_and_clean_data('data/creditcard.csv')
    return df

try:
    df = load_data()
    stats = get_basic_stats(df)
    impact = calculate_financial_impact(df)
    
    # Row 1: Key Performance Indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Transactions",
            value=f"{stats['total_transactions']:,}"
        )
    
    with col2:
        st.metric(
            label="💵 Total Amount",
            value=f"${stats['total_amount']:,.0f}"
        )
    
    with col3:
        st.metric(
            label="⚠️ Fraud Transactions",
            value=f"{stats['fraud_transactions']:,}",
            delta=f"{stats['fraud_rate']:.3f}% of total",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="💸 Fraud Loss",
            value=f"${stats['fraud_amount']:,.0f}",
            delta=f"{stats['fraud_amount_percent']:.2f}% of total",
            delta_color="inverse"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Fraud Transactions Timeline")
        fig_timeline = create_fraud_timeline(df)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        st.subheader("📊 Amount Distribution")
        fig_amount = create_amount_distribution(df)
        st.plotly_chart(fig_amount, use_container_width=True)
    
    st.markdown("---")
    
    # Row 3: Quick Insights
    st.subheader("🔍 Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        ### 📌 Risk Summary
        - **Fraud Rate**: {stats['fraud_rate']:.4f}% of transactions
        - **Average Fraud Loss**: ${impact['avg_loss_per_fraud']:.2f} per transaction
        - **Maximum Loss**: ${impact['max_fraud_amount']:.2f} in one transaction
        """)
    
    with col2:
        st.warning(f"""
        ### ⚠️ Areas to Monitor
        - Fraud losses represent {impact['loss_percentage']:.2f}% of total amount
        - Average normal transaction: ${stats['avg_normal_amount']:.2f}
        """)
    
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.exception(e)