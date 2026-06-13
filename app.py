import streamlit as st
import pandas as pd
import numpy as np

# --- Generate synthetic transaction data ---
def generate_data(n=100):
    np.random.seed(42)
    data = {
        "TransactionID": range(1, n+1),
        "AccountNumber": np.random.randint(1000, 1100, n),
        "AmountUGX": np.random.randint(1000, 20000000, n),
        "PhoneNumber": np.random.choice(["0771234567","0787654321","0751112222","0709998888"], n),
        "Timestamp": pd.date_range("2024-01-01", periods=n, freq="h")
    }
    df = pd.DataFrame(data)
    return df

# --- Fraud detection rules ---
def detect_fraud(df):
    df["Flagged"] = False
    df["Reason"] = ""

    # Rule 1: Large transaction
    df.loc[df["AmountUGX"] > 10000000, ["Flagged","Reason"]] = [True,"High amount"]

    # Rule 2: Duplicate phone number with multiple accounts
    dupes = df.groupby("PhoneNumber")["AccountNumber"].nunique()
    risky_numbers = dupes[dupes > 1].index
    df.loc[df["PhoneNumber"].isin(risky_numbers), ["Flagged","Reason"]] = [True,"Duplicate accounts"]

    # Rule 3: Sudden spike (mock rule: >3 transactions in 1 hour)
    counts = df.groupby(df["Timestamp"].dt.hour)["TransactionID"].count()
    risky_hours = counts[counts > 3].index
    df.loc[df["Timestamp"].dt.hour.isin(risky_hours), ["Flagged","Reason"]] = [True,"Spike in activity"]

    return df

# --- Streamlit UI ---
st.title("💳 Fraud Detection Demo")
st.write("Prototype fraud detection tool for Bank of Uganda Hackathon")

# Generate and detect
df = generate_data(50)
df = detect_fraud(df)

# Show flagged transactions
st.subheader("Suspicious Transactions")
st.dataframe(df[df["Flagged"]])

# Show summary chart
st.subheader("Fraud Summary")
summary = df["Reason"].value_counts()
st.bar_chart(summary)

