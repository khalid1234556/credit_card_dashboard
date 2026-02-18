"""
Fraud Analysis page - analyzes fraud patterns
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_and_clean_data

# Configure page
st.set_page_config(page_title="Fraud Analysis", page_icon="⚠️", layout="wide")

st.title("⚠️ Fraud Transaction Analysis")
st.markdown("Understanding fraud patterns and characteristics")

# Load data
@st.cache_data
def load_data():
    return load_and_clean_data('data/creditcard.csv')

df = load_data()

# Separate fraud and normal transactions
fraud_df = df[df['Class'] == 1]
normal_df = df[df['Class'] == 0]

if len(fraud_df) == 0:
    st.warning("No fraud transactions found in the data!")
    st.stop()

# Quick stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Fraud Transactions", f"{len(fraud_df):,}")
with col2:
    st.metric("Percentage of Total", f"{(len(fraud_df)/len(df))*100:.4f}%")
with col3:
    st.metric("Total Loss", f"${fraud_df['Amount'].sum():,.0f}")
with col4:
    st.metric("Maximum Loss", f"${fraud_df['Amount'].max():,.2f}")

# Comparison chart
st.subheader("📊 Normal vs Fraud Comparison")

comparison_df = pd.DataFrame({
    'Type': ['Normal', 'Fraud'],
    'Count': [len(normal_df), len(fraud_df)],
    'Average Amount': [normal_df['Amount'].mean(), fraud_df['Amount'].mean()]
})

col1, col2 = st.columns(2)

with col1:
    fig_count = px.bar(
        comparison_df,
        x='Type',
        y='Count',
        color='Type',
        color_discrete_map={'Normal': 'green', 'Fraud': 'red'},
        title='Transaction Count Comparison'
    )
    st.plotly_chart(fig_count, use_container_width=True)

with col2:
    fig_amount = px.bar(
        comparison_df,
        x='Type',
        y='Average Amount',
        color='Type',
        color_discrete_map={'Normal': 'green', 'Fraud': 'red'},
        title='Average Amount Comparison'
    )
    st.plotly_chart(fig_amount, use_container_width=True)

# Hourly fraud distribution
st.subheader("🕐 Fraud Distribution by Hour")

fraud_by_hour = fraud_df.groupby('Hour').size().reset_index(name='count')
fraud_by_hour['Hour'] = fraud_by_hour['Hour'].astype(int)

fig = px.line(
    fraud_by_hour,
    x='Hour',
    y='count',
    title='Fraud Transactions by Hour',
    markers=True
)
fig.update_traces(line_color='red', line_width=3)
st.plotly_chart(fig, use_container_width=True)

# Amount category analysis
st.subheader("💰 Fraud by Amount Category")

fraud_by_category = fraud_df.groupby('Amount_Category').size().reset_index(name='count')
fraud_by_category['percentage'] = (fraud_by_category['count'] / fraud_by_category['count'].sum()) * 100

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        fraud_by_category,
        values='count',
        names='Amount_Category',
        title='Fraud Distribution by Amount Category',
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.dataframe(
        fraud_by_category[['Amount_Category', 'count', 'percentage']].round(2),
        use_container_width=True,
        hide_index=True,
        column_config={
            'Amount_Category': 'Amount Category',
            'count': 'Count',
            'percentage': 'Percentage (%)'
        }
    )

# Top fraud transactions
st.subheader("💰 Top 10 Fraud Transactions")

top_frauds = fraud_df.nlargest(10, 'Amount')[['Amount', 'Hour', 'Amount_Category']]
top_frauds['Amount'] = top_frauds['Amount'].apply(lambda x: f"${x:,.2f}")

st.dataframe(
    top_frauds,
    use_container_width=True,
    hide_index=True,
    column_config={
        'Amount': 'Amount',
        'Hour': 'Hour',
        'Amount_Category': 'Category'
    }
)

# Insights
if len(fraud_by_hour) > 0 and len(fraud_by_category) > 0:
    st.subheader("🔍 Key Findings")
    st.markdown(f"""
    - **Average Fraud Amount**: ${fraud_df['Amount'].mean():.2f} ({(fraud_df['Amount'].mean()/normal_df['Amount'].mean()):.1f}x larger than normal)
    - **Peak Fraud Hour**: {int(fraud_by_hour.loc[fraud_by_hour['count'].idxmax(), 'Hour'])}:00
    - **Highest Risk Category**: {fraud_by_category.loc[fraud_by_category['count'].idxmax(), 'Amount_Category']}
    """)