import streamlit as st
import pandas as pd
import os

def personal_insights(df, user_id):
    summary = "Personal Insights:\n"

    # Monthly expenses
    if "expense" in df.columns and "month" in df.columns:
        monthly = df.groupby("month")["expense"].sum().to_dict()
        summary += f"- Monthly expenses: {monthly}\n"

    # Weight trend
    if "weight" in df.columns and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df_sorted = df.sort_values("date")
        avg_weight = df_sorted["weight"].mean()
        summary += f"- Average weight: {avg_weight:.1f}\n"
        if len(df_sorted) > 1:
            change = df_sorted["weight"].iloc[-1] - df_sorted["weight"].iloc[0]
            summary += f"- Weight change over time: {change:+.1f}\n"

    # Save to file
    folder = f"data_storage/user_{user_id}/insights"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/personal_insights.txt","w") as f:
        f.write(summary)

    return summary

def show_personal_insights():
    df = st.session_state.get("data")
    user = st.session_state.get("user")
    if df is None or not user:
        st.warning("Upload data first.")
        return
    summary = personal_insights(df, user["id"])
    st.write(summary)