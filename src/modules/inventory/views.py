import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression

def show_inventory():
    st.subheader("Inventory Management")
    user = st.session_state.get("user")
    file = st.file_uploader("Upload Inventory CSV (columns: item, quantity, price, delivery_date, sales_per_day, reorder_level, max_stock)")

    if file and user:
        df = pd.read_csv(file)
        st.session_state["inventory"] = df

        folder = f"data_storage/user_{user['id']}/inventory"
        os.makedirs(folder, exist_ok=True)
        df.to_csv(f"{folder}/inventory.csv", index=False)

        st.write("Current Inventory")
        st.dataframe(df)

        # Analytics
        st.subheader("Inventory Analytics")
        total_items = df["quantity"].sum()
        total_value = (df["quantity"] * df["price"]).sum()
        st.write(f"Total items in stock: {total_items}")
        st.write(f"Total inventory value: {total_value:.2f}")

        # Low stock alert
        low_stock = df[df["quantity"] < df["reorder_level"]]
        if not low_stock.empty:
            st.warning("Low stock items (need reorder):")
            st.dataframe(low_stock)

        # Overstock alert
        overstock = df[df["quantity"] > df["max_stock"]]
        if not overstock.empty:
            st.error("Overstocked items:")
            st.dataframe(overstock)

        # Delayed stocks
        if "delivery_date" in df:
            df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")
            delayed = df[df["delivery_date"] < pd.Timestamp.today()]
            if not delayed.empty:
                st.warning("Delayed stock items:")
                st.dataframe(delayed)

        # Forecasting
        if "sales_per_day" in df:
            st.subheader("Forecasting")
            df["days_to_depletion"] = df["quantity"] / df["sales_per_day"].replace(0, np.nan)
            st.write("Estimated days until stock depletion:")
            st.dataframe(df[["item","days_to_depletion"]])

            # Regression forecast
            X = df[["sales_per_day"]]
            y = df["quantity"]
            model = LinearRegression()
            model.fit(X,y)
            forecast = model.predict([[10]])  # example scenario
            st.info(f"Forecasted inventory if sales_per_day=10: {forecast[0]:.0f} units")

        # Automated reorder suggestions
        st.subheader("Reorder Suggestions")
        reorder_suggestions = df[df["quantity"] < df["reorder_level"]]
        if not reorder_suggestions.empty:
            st.write("Suggested items to reorder:")
            for _, row in reorder_suggestions.iterrows():
                reorder_qty = row["max_stock"] - row["quantity"]
                st.write(f"- {row['item']}: reorder {reorder_qty} units")