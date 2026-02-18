"""
Main application entry point
"""
import streamlit as st
from utils.data_loader import load_and_clean_data

# Configure the page settings
# Set up the dashboard layout, title, and sidebar
st.set_page_config(
    page_title="Credit Card Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data with loading spinner
# Show a spinner while data is being downloaded from the online source
with st.spinner("Loading data from online source..."):
    try:
        # Call the function that loads data directly from URL
        # No file path needed anymore - data comes from GitHub
        df = load_and_clean_data()
        
        # Store data in session state so it persists across pages
        st.session_state['data_loaded'] = True
        st.session_state['df'] = df
    except Exception as e:
        # If loading fails, show error message
        st.session_state['data_loaded'] = False
        st.error(f"❌ Failed to load data: {e}")
        st.info("Please check your internet connection. The data is loaded from GitHub.")

# Main page content
st.title("💳 Credit Card Risk Dashboard")
st.markdown("""
### Welcome to the Dashboard

This dashboard helps you monitor and analyze credit card fraud risk.

👈 Select a page from the sidebar to begin
""")

# Show quick stats if data is loaded successfully
if st.session_state.get('data_loaded', False):
    df = st.session_state['df']
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Display total number of transactions
        st.info(f"📊 **Total Transactions**: {len(df):,}")
    
    with col2:
        # Calculate and display fraud transactions count and percentage
        fraud_count = df['Class'].sum()
        st.warning(f"⚠️ **Fraud Transactions**: {fraud_count:,} ({(fraud_count/len(df))*100:.4f}%)")
    
    with col3:
        # Display total amount of all transactions
        st.success(f"💰 **Total Amount**: ${df['Amount'].sum():,.0f}")
    
    # Add a small caption showing data source
    st.caption("📌 Data loaded from: GitHub repository (online source)")
else:
    # Show warning if data couldn't be loaded
    st.warning("⚠️ Could not load data. Please check your internet connection.")