# 💳 Credit Card Fraud Risk & Financial Impact Dashboard

**Live Dashboard**: [https://creditcarddashboard-heztqfmp73wjnjytqgqe9u.streamlit.app/](https://creditcarddashboard-heztqfmp73wjnjytqgqe9u.streamlit.app/)

## 1. Project Overview

This is an interactive dashboard that analyzes credit card transaction data to identify fraud patterns and financial impact. The dashboard helps decision-makers understand fraud risks and take data-driven actions.

**Main Question**: How can financial institutions monitor fraud risk and minimize financial losses?

## 2. Data Source

**Dataset**: Credit Card Fraud Detection Dataset from Kaggle  
**Link**: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

**What's in the data**:
- 284,807 transactions
- 28 anonymized features (PCA transformed)
- Time (in seconds)
- Amount
- Class (0 = Normal, 1 = Fraud)

## 3. Methodology

### Data Preparation
- Loaded CSV file using pandas
- Removed duplicates and null values
- Added new columns for better analysis:
  - `Transaction_Type`: Normal/Fraud (text labels)
  - `Hour`: Converted time to hours
  - `Amount_Category`: Grouped amounts into categories

### Analysis Approach
- Focused on business perspective, not technical
- Analyzed temporal patterns
- Compared normal vs fraud behavior
- Calculated financial impact

### Tool Selection
- **Streamlit**: For interactive dashboard
- **Plotly**: For interactive charts
- **Pandas**: For data manipulation

## 4. Dashboard Structure

### Executive Overview
High-level KPIs for management:
- Total transactions and amounts
- Fraud statistics
- Financial losses

### Transaction Analysis
Understanding normal customer behavior:
- Hourly patterns
- Amount distributions
- Category analysis

### Fraud Analysis
Analyzing fraud characteristics:
- Fraud patterns by hour
- Amount comparison
- Top fraud transactions

### Risk Insights
Business recommendations:
- Risk metrics
- Action plans
- Strategic recommendations

## 5. Key Insights

1. Fraud is rare but expensive (0.17% of transactions, 0.8% of total amount)
2. Fraud transactions are 5x larger than normal transactions
3. Most fraud occurs during late night hours (2 AM peak)
4. Large transactions (> $1000) carry the highest risk
5. 10 transactions account for 25% of total fraud loss

## 6. Recommendations

### Immediate Actions
- Monitor transactions > $1000
- Increase nighttime monitoring
- Real-time customer alerts

### Short-term Actions
- Build ML detection model
- Train review team
- Implement behavioral analysis

### Strategic Actions
- Real-time fraud detection
- Advanced analytics
- Industry collaboration

## 7. How to Run Locally

```bash
# Clone repository
git https://github.com/khalid1234556/credit_card_dashboard.git
cd credit-card-dashboard

# Install dependencies
pip install -r requirements.txt

# Download data from Kaggle and place in data/ folder

# Run the app
streamlit run app.py