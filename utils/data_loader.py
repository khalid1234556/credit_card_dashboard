"""
Handles data loading and cleaning operations
"""
import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data(file_path):
    """
    Loads CSV file and performs data cleaning
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Remove any rows with missing values
    df = df.dropna()
    
    # Remove duplicate rows if they exist
    df = df.drop_duplicates()
    
    # Create a new column with readable transaction type (Normal/Fraud)
    df['Transaction_Type'] = df['Class'].map({0: 'Normal', 1: 'Fraud'})
    
    # Convert time from seconds to hours (24-hour format)
    df['Hour'] = (df['Time'] / 3600) % 24
    
    # Create amount in thousands for better readability
    df['Amount_K'] = df['Amount'] / 1000
    
    # Categorize amounts into meaningful groups
    def categorize_amount(amount):
        if amount < 100:
            return 'Small (< $100)'
        elif amount < 500:
            return 'Medium ($100-$500)'
        elif amount < 1000:
            return 'Large ($500-$1000)'
        else:
            return 'Very Large (> $1000)'
    
    df['Amount_Category'] = df['Amount'].apply(categorize_amount)
    
    return df

def get_basic_stats(df):
    """
    Calculates basic statistics from the dataframe
    """
    total_transactions = len(df)
    fraud_transactions = df['Class'].sum()
    normal_transactions = total_transactions - fraud_transactions
    total_amount = df['Amount'].sum()
    fraud_amount = df[df['Class'] == 1]['Amount'].sum() if fraud_transactions > 0 else 0
    
    # Create normal_df for average calculation
    normal_df = df[df['Class'] == 0]
    
    stats = {
        'total_transactions': total_transactions,
        'fraud_transactions': int(fraud_transactions),
        'normal_transactions': int(normal_transactions),
        'fraud_rate': (fraud_transactions / total_transactions) * 100 if total_transactions > 0 else 0,
        'total_amount': total_amount,
        'fraud_amount': fraud_amount,
        'fraud_amount_percent': (fraud_amount / total_amount) * 100 if total_amount > 0 else 0,
        'avg_normal_amount': normal_df['Amount'].mean() if len(normal_df) > 0 else 0
    }
    
    return stats