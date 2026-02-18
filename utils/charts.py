"""
Creates interactive charts using Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_fraud_timeline(df):
    """
    Creates a line chart showing fraud distribution over 24 hours
    """
    # Count fraud transactions per hour
    fraud_by_hour = df[df['Class'] == 1].groupby('Hour').size().reset_index(name='count')
    
    # Create line chart
    fig = px.line(
        fraud_by_hour,
        x='Hour',
        y='count',
        title='Fraud Transactions by Hour',
        markers=True
    )
    
    # Customize the chart
    fig.update_traces(line_color='red', line_width=3)
    fig.update_layout(
        xaxis_title='Hour of Day',
        yaxis_title='Number of Fraud Transactions',
        hovermode='x unified'
    )
    
    return fig

def create_amount_distribution(df):
    """
    Creates histogram comparing normal vs fraud amounts
    """
    # Create subplot with two charts side by side
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Normal Transactions', 'Fraud Transactions')
    )
    
    # Get amounts for normal and fraud transactions
    normal_amounts = df[df['Class'] == 0]['Amount']
    fraud_amounts = df[df['Class'] == 1]['Amount']
    
    # Add normal transactions histogram
    fig.add_trace(
        go.Histogram(x=normal_amounts, nbinsx=50, name='Normal', marker_color='green'),
        row=1, col=1
    )
    
    # Add fraud transactions histogram
    fig.add_trace(
        go.Histogram(x=fraud_amounts, nbinsx=50, name='Fraud', marker_color='red'),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title='Amount Distribution: Normal vs Fraud',
        height=400,
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Amount ($)", row=1, col=1)
    fig.update_xaxes(title_text="Amount ($)", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    
    return fig

def create_fraud_heatmap(df):
    """
    Creates heatmap showing fraud rate by hour and amount category
    """
    # Create amount bins
    df_copy = df.copy()
    df_copy['Amount_Bin'] = pd.cut(
        df_copy['Amount'], 
        bins=[0, 100, 500, 1000, 5000], 
        labels=['0-100', '100-500', '500-1000', '>1000']
    )
    
    # Create pivot table for heatmap
    heatmap_data = df_copy.pivot_table(
        values='Class',
        index='Amount_Bin',
        columns=pd.cut(df_copy['Hour'], bins=24, labels=[f'{i:02d}' for i in range(24)]),
        aggfunc='mean'
    ).fillna(0)
    
    # Create heatmap
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Hour", y="Amount Category", color="Fraud Rate"),
        color_continuous_scale='Reds',
        aspect="auto"
    )
    
    fig.update_layout(
        title='Fraud Rate Heatmap: Hour vs Amount',
        height=400
    )
    
    return fig