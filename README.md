# 💳 Credit Card Fraud Risk & Financial Impact Dashboard

**Live Dashboard**: [https://creditcarddashboard-heztqfmp73wjnjytqgqe9u.streamlit.app/](https://creditcarddashboard-heztqfmp73wjnjytqgqe9u.streamlit.app/)

---

## 1. Project Overview

This is an interactive dashboard that analyzes credit card transaction data to identify fraud patterns and financial impact. The dashboard helps decision-makers understand fraud risks and take data-driven actions.

**Main Question**: How can financial institutions monitor fraud risk and minimize financial losses?

---

## 2. Data Source

**Dataset**: Credit Card Fraud Detection Dataset from Kaggle  
**Link**: [https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

**What's in the data**:
- 284,807 transactions
- 28 anonymized features (PCA transformed)
- Time (in seconds)
- Amount
- Class (0 = Normal, 1 = Fraud)

---

## 3. Methodology

### Data Preparation
- Loaded CSV file using pandas
- Removed duplicates and null values
- Added new columns for better analysis:
  - `Transaction_Type`: Normal/Fraud (text labels)
  - `Hour`: Converted time to hours
  - `Amount_Category`: Grouped amounts into categories

### Analysis Approach
- Focused on business perspective, not purely technical metrics
- Analyzed behavioral and temporal patterns
- Compared normal vs fraud behavior
- Calculated financial impact

### Tool Selection
- **Streamlit**: Interactive dashboard
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation

---

## 4. Dashboard Structure

### Executive Overview
High-level KPIs for management:
- Total transactions and processed amounts
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
Business interpretation:
- Risk indicators
- Action plans
- Operational recommendations

---

## 5. Key Insights

- Fraud is rare but expensive (0.17% of transactions, 0.8% of total amount)
- Fraud transactions are 5× larger than normal transactions
- Most fraud occurs during late night hours (2 AM peak)
- Large transactions (> $1000) carry the highest risk
- 10 transactions account for 25% of total fraud loss

---

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
- Real-time fraud detection infrastructure
- Advanced analytics
- Industry collaboration

---

## 7. Operational Decision Rules

Based on observed fraud behavior, the following operational controls are proposed to reduce losses while maintaining customer experience.

### Automatic Protection Rules (Real-Time Controls)

| Scenario | Action |
|----------|--------|
| Transactions above $3000 between 01:00–05:00 | Temporary hold |
| Transactions above $1000 at night | OTP verification |
| More than 3 transactions within 60 seconds | Temporary card freeze |
| First transaction in new country + amount > $800 | OTP verification |
| Spending greater than 5× customer normal average | Step-up authentication |

### Manual Review Queue (Fraud Analyst Team)

Route transactions to human investigation instead of immediate blocking:
- Amount > $1000 during unusual hour
- Rapid spending after inactivity
- Multiple declined attempts followed by approval
- High-risk merchant category combined with high amount

### Low-Risk Allowed Transactions

To maintain customer experience, the following should not trigger alerts:
- Recurring subscriptions and known merchants
- Small daytime purchases
- Normal spending patterns consistent with history

### Expected Operational Impact

Focus monitoring on less than 2% of transactions while targeting the majority of fraud losses. This significantly reduces investigation workload and prevents major financial damage before settlement.

---

## 8. Business Value

This dashboard provides measurable financial value by helping institutions focus monitoring efforts where fraud risk is highest instead of reviewing all transactions equally.

By identifying that 25% of fraud losses originate from only 10 transactions, institutions can apply targeted controls (alerts and manual verification) to a very small subset of operations — reducing operational cost while preventing major losses.

Monitoring high-amount nighttime transactions allows early intervention before settlement, reducing chargebacks and customer disputes.

**Expected Impact**:
- Reduce fraud losses
- Lower investigation workload
- Improve customer trust
- Maintain smooth experience for legitimate users

---

## 9. Conclusion

This project demonstrates how analytical insights can be translated into operational financial policies rather than static reporting.

The dashboard is not only descriptive but prescriptive — enabling financial institutions to act proactively instead of reacting after fraud occurs.

The goal is transforming fraud monitoring from a reactive investigation process into a real-time risk prevention strategy.

---

## 10. How to Run Locally

```bash
# Clone repository
git clone https://github.com/khalid1234556/credit_card_dashboard.git
cd credit_card_dashboard

# Install dependencies
pip install -r requirements.txt

# Download data from Kaggle and place in data/ folder

# Run the app
streamlit run app.py
```