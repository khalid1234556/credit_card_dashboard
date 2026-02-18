"""
Transaction Analysis page - analyzes normal customer behavior
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_and_clean_data

# Configure page
st.set_page_config(page_title="Transaction Analysis", page_icon="📊", layout="wide")

st.title("📊 Transaction Analysis")
st.markdown("Analyzing normal customer behavior patterns")

# Load data
@st.cache_data
def load_data():
    return load_and_clean_data()

df = load_data()

# Filter for normal transactions only
normal_df = df[df['Class'] == 0]

# Sidebar filters
st.sidebar.header("🔍 Analysis Filters")

amount_range = st.sidebar.slider(
    "Amount Range ($)",
    min_value=0,
    max_value=int(df['Amount'].max()),
    value=(0, int(df['Amount'].max()))
)

hour_range = st.sidebar.slider(
    "Hour Range",
    min_value=0,
    max_value=23,
    value=(0, 23)
)

# Apply filters
filtered_df = normal_df[
    (normal_df['Amount'] >= amount_range[0]) &
    (normal_df['Amount'] <= amount_range[1]) &
    (normal_df['Hour'] >= hour_range[0]) &
    (normal_df['Hour'] <= hour_range[1])
]

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Normal Transactions", f"{len(filtered_df):,}")
with col2:
    st.metric("Average Amount", f"${filtered_df['Amount'].mean():.2f}")
with col3:
    st.metric("Total Amount", f"${filtered_df['Amount'].sum():,.0f}")

# Hourly distribution chart
st.subheader("🕐 Customer Activity Throughout the Day")

hourly_data = filtered_df.groupby('Hour').size().reset_index(name='count')

fig = px.bar(
    hourly_data,
    x='Hour',
    y='count',
    title='Transactions by Hour',
    labels={'Hour': 'Hour of Day', 'count': 'Number of Transactions'},
    color='count',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig, use_container_width=True)

# Amount category analysis
st.subheader("💰 Amount Category Analysis")

category_stats = filtered_df.groupby('Amount_Category').size().reset_index(name='count')
category_stats['percentage'] = (category_stats['count'] / category_stats['count'].sum()) * 100

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        category_stats,
        values='count',
        names='Amount_Category',
        title='Transaction Distribution by Amount Category'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.dataframe(
        category_stats[['Amount_Category', 'count', 'percentage']].round(2),
        use_container_width=True,
        hide_index=True,
        column_config={
            'Amount_Category': 'Amount Category',
            'count': 'Count',
            'percentage': 'Percentage (%)'
        }
    )

# Summary statistics
st.subheader("📊 Summary Statistics")
st.dataframe(
    filtered_df['Amount'].describe().round(2),
    use_container_width=True
)