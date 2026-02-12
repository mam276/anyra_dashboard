import pandas as pd
import os
import streamlit as st
from .retention import retention_kpis
from .predictive_retention import predict_churn

def show_analytics():
    st.subheader("Analytics")
    user = st.session_state.get("user")
    df = st.session_state.get("data")

    if df is None or not user:
        st.warning("Upload data first.")
        return

    kpis = calculate_kpis(df, user["id"], user["role"], user.get("industry","generic"))
    st.json(kpis)

    retention = retention_kpis(df)
    st.json(retention)

    if st.button("Run Predictive Retention Model"):
        predictions = predict_churn(df, user["id"])
        st.write(predictions)

def calculate_kpis(df, user_id, role="client", industry="generic"):
    kpis = {"rows": len(df), "columns": len(df.columns)}
    if role == "client":
        if industry == "retail" and "sales" in df:
            kpis["total_sales"] = df["sales"].sum()
    folder = f"data_storage/user_{user_id}/analytics"
    os.makedirs(folder, exist_ok=True)
    pd.DataFrame([kpis]).to_csv(f"{folder}/kpis.csv", index=False)
    return kpis