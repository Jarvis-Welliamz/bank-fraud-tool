import streamlit as st
import pandas as pd

# Load transactions from CSV
@st.cache_data
def load_data():
    return pd.read_csv("transactions.csv")
    df.columns = df.columns.str.strip()

# Fraud detection rules
def detect_fraud(df):
    flagged = []
    duplicate_mask = df["Customer Name"].duplicated(keep=False)

    for idx, row in df.iterrows():
        reasons = []

        # Rule 1: High-value transactions
        if row["Amount"] > 2000:
            reasons.append("High-value transaction")

        # Rule 2: Suspicious merchants
        if row["Merchant"] in ["Luxury Cars", "Jewelry Store", "Travel Agency"]:
            reasons.append("Suspicious merchant")

        # Rule 3: Duplicate customer names (same Name used multiple times)
        if duplicate_mask.iloc[idx]:
            reasons.append("Duplicate customer")

        if reasons:
            flagged.append({
                "Merchant": row["Merchant"],
                "Amount": row["Amount"],
                "Location": row["Location"],
                "Customer Name": row["Customer Name"],
                "Timestamp": row["Timestamp"],
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

