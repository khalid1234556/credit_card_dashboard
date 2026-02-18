"""
Calculates financial metrics and risk indicators
"""
import pandas as pd

def calculate_risk_metrics(df):
    """
    Calculates risk-related metrics from fraud data
    """
    fraud_df = df[df['Class'] == 1]
    normal_df = df[df['Class'] == 0]
    
    metrics = {}
    
    # Average amounts comparison
    metrics['avg_fraud_amount'] = fraud_df['Amount'].mean() if len(fraud_df) > 0 else 0
    metrics['avg_normal_amount'] = normal_df['Amount'].mean() if len(normal_df) > 0 else 0
    metrics['max_fraud_amount'] = fraud_df['Amount'].max() if len(fraud_df) > 0 else 0
    
    # Calculate ratio of fraud to normal amounts
    if metrics['avg_normal_amount'] > 0:
        metrics['fraud_to_normal_ratio'] = metrics['avg_fraud_amount'] / metrics['avg_normal_amount']
    else:
        metrics['fraud_to_normal_ratio'] = 0
    
    # Find busiest hour for fraud
    if len(fraud_df) > 0:
        fraud_by_hour = fraud_df.groupby('Hour').size()
        busiest_hour = fraud_by_hour.idxmax()
        metrics['busiest_fraud_hour'] = int(busiest_hour)
    else:
        metrics['busiest_fraud_hour'] = None
    
    return metrics

def calculate_financial_impact(df):
    """
    Calculates the financial impact of fraud
    """
    fraud_df = df[df['Class'] == 1]
    
    impact = {
        'total_fraud_loss': fraud_df['Amount'].sum(),
        'total_transactions_volume': df['Amount'].sum(),
        'avg_loss_per_fraud': fraud_df['Amount'].mean() if len(fraud_df) > 0 else 0,
        'max_fraud_amount': fraud_df['Amount'].max() if len(fraud_df) > 0 else 0
    }
    
    # Calculate loss percentage
    if impact['total_transactions_volume'] > 0:
        impact['loss_percentage'] = (impact['total_fraud_loss'] / impact['total_transactions_volume']) * 100
    else:
        impact['loss_percentage'] = 0
    
    return impact