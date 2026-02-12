import streamlit as st
import plotly.express as px

def show_visualization():
    st.subheader("Visualization")
    df = st.session_state.get("data")
    if df is None:
        st.warning("Upload data first.")
        return

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        col = st.selectbox("Select column to visualize", numeric_cols)
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig)