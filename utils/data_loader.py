"""
Handles data loading and cleaning operations
"""
import pandas as pd
import streamlit as st
import requests
from io import BytesIO

@st.cache_data
def load_and_clean_data():
    """
    Loads data directly from URL (no files in repo)
    """
    # URL for the credit card fraud dataset from GitHub repository
    # This URL points to a raw CSV file hosted on GitHub
    url = "https://raw.githubusercontent.com/nsethi31/Kaggle-Data-Credit-Card-Fraud-Detection/master/creditcard.csv"
    
    # Download the data from the URL
    # requests.get() fetches the file content
    response = requests.get(url)
    
    # Convert the response content to a pandas DataFrame
    # BytesIO is used to handle the binary data
    df = pd.read_csv(BytesIO(response.content))
    
    # Remove any rows with missing values
    # This ensures data quality for analysis
    df = df.dropna()
    
    # Remove duplicate rows if they exist
    # Duplicates can skew analysis results
    df = df.drop_duplicates()
    
    # Create a new column with readable transaction type
    # Map 0 to 'Normal' and 1 to 'Fraud' for better understanding
    df['Transaction_Type'] = df['Class'].map({0: 'Normal', 1: 'Fraud'})
    
    # Convert time from seconds to hours (24-hour format)
    # Original time is in seconds from first transaction
    # Dividing by 3600 converts to hours, % 24 gives hour of day
    df['Hour'] = (df['Time'] / 3600) % 24
    
    # Create amount in thousands for better readability
    # Large numbers are easier to read in thousands
    df['Amount_K'] = df['Amount'] / 1000
    
    # Helper function to categorize amounts into meaningful groups
    def categorize_amount(amount):
        if amount < 100:
            return 'Small (< $100)'
        elif amount < 500:
            return 'Medium ($100-$500)'
        elif amount < 1000:
            return 'Large ($500-$1000)'
        else:
            return 'Very Large (> $1000)'
    
    # Apply the categorization function to create new column
    df['Amount_Category'] = df['Amount'].apply(categorize_amount)
    
    return df

def get_basic_stats(df):
    """
    Calculates basic statistics from the dataframe
    """
    # Total number of transactions
    total_transactions = len(df)
    
    # Number of fraud transactions (Class = 1)
    fraud_transactions = df['Class'].sum()
    
    # Number of normal transactions
    normal_transactions = total_transactions - fraud_transactions
    
    # Total amount of all transactions
    total_amount = df['Amount'].sum()
    
    # Total amount of fraud transactions
    fraud_amount = df[df['Class'] == 1]['Amount'].sum() if fraud_transactions > 0 else 0
    
    # DataFrame containing only normal transactions
    normal_df = df[df['Class'] == 0]
    
    # Dictionary containing all statistics
    stats = {
        # Transaction counts
        'total_transactions': total_transactions,
        'fraud_transactions': int(fraud_transactions),
        'normal_transactions': int(normal_transactions),
        
        # Fraud rate as percentage
        'fraud_rate': (fraud_transactions / total_transactions) * 100 if total_transactions > 0 else 0,
        
        # Amount statistics
        'total_amount': total_amount,
        'fraud_amount': fraud_amount,
        'fraud_amount_percent': (fraud_amount / total_amount) * 100 if total_amount > 0 else 0,
        
        # Average normal transaction amount
        'avg_normal_amount': normal_df['Amount'].mean() if len(normal_df) > 0 else 0
    }
    
    return stats