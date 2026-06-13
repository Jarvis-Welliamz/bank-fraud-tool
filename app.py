import streamlit as st
import pandas as pd

# Load transactions from CSV
@st.cache_data
def load_data():
    return pd.read_csv("transactions.csv")

# Fraud detection rules
def detect_fraud(df):
    flagged = []

    for idx, row in df.iterrows():
        reasons = []

        # Rule 1: High-value transactions
        if row["Amount"] > 2000:
            reasons.append("High-value transaction")

        # Rule 2: Suspicious merchants
        if row["Merchant"] in ["Luxury Cars", "Jewelry Store", "Travel Agency"]:
            reasons.append("Suspicious merchant")

        # Rule 3: Duplicate names (same Name used multiple times)
        if df["Name"].duplicated(keep=False)[idx]:
            reasons.append("Duplicate customer")

        if reasons:
            flagged.append({
                "TransactionID": row["TransactionID"],
                "Amount": row["Amount"],
                "Merchant": row["Merchant"],
                "Location": row["Location"],
                "Name": row["Name"],
                "Date": row["Date"],
                "Flagged": "☑",
                "Reason": ", ".join(reasons)
            })

    return pd.DataFrame(flagged)

# Streamlit UI
st.title("Suspicious Transactions")

df = load_data()
st.subheader("All Transactions")
st.dataframe(df)

fraud_df = detect_fraud(df)
st.subheader("Flagged Transactions")
st.dataframe(fraud_df)

