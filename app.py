"""
Main application entry point
"""
import streamlit as st
from utils.data_loader import load_and_clean_data

# Configure the page settings
st.set_page_config(
    page_title="Credit Card Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data with loading spinner
with st.spinner("Loading data..."):
    try:
        df = load_and_clean_data('data/creditcard.csv')
        st.session_state['data_loaded'] = True
        st.session_state['df'] = df
    except Exception as e:
        st.session_state['data_loaded'] = False
        st.error(f"Failed to load data: {e}")

# Main page content
st.title("💳 Credit Card Risk Dashboard")
st.markdown("""
### Welcome to the Dashboard

This dashboard helps you monitor and analyze credit card fraud risk.

👈 Select a page from the sidebar to begin
""")

# Show quick stats if data is loaded
if st.session_state.get('data_loaded', False):
    df = st.session_state['df']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"📊 **Total Transactions**: {len(df):,}")
    with col2:
        fraud_count = df['Class'].sum()
        st.warning(f"⚠️ **Fraud Transactions**: {fraud_count:,} ({(fraud_count/len(df))*100:.4f}%)")
    with col3:
        st.success(f"💰 **Total Amount**: ${df['Amount'].sum():,.0f}")