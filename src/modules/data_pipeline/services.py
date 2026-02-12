import pandas as pd
import os
import streamlit as st

def show_data_pipeline():
    st.subheader("Data Pipeline")
    user = st.session_state.get("user")
    file = st.file_uploader("Upload CSV/XLSX/JSON")

    if file and user:
        df = load_data(file)
        cleaned = clean_data(df, user["id"])
        st.session_state["data"] = cleaned
        st.success("File uploaded and cleaned successfully.")

def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    elif file.name.endswith(".json"):
        return pd.read_json(file)
    return None

def clean_data(df, user_id):
    df = df.dropna(how="all").drop_duplicates().fillna(0)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    folder = f"data_storage/user_{user_id}/cleaned"
    os.makedirs(folder, exist_ok=True)
    df.to_csv(f"{folder}/cleaned_data.csv", index=False)
    return df