import os
import streamlit as st

INSIGHT_REGISTRY = {
    "financial": {"total_sales": ["sales"], "portfolio_value": ["value"]},
    "customer": {"unique_customers": ["customer_id"], "churn_rate": ["churn"]},
    "personal": {"monthly_expenses": ["expense","month"], "weight_trend": ["weight","date"]},
    "inventory": {"stock_levels": ["item","quantity","price"]}
}

def adaptive_insights(df, user_id, industry="generic"):
    summary = f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.\n"
    cols = df.columns.tolist()

    if "sales" in cols:
        summary += f"Total sales: {df['sales'].sum()}.\n"
    if "customer_id" in cols:
        summary += f"Unique customers: {df['customer_id'].nunique()}.\n"
    if "churn" in cols:
        summary += f"Churn rate: {df['churn'].mean()*100:.1f}%.\n"
    if "expense" in cols and "month" in cols:
        monthly = df.groupby("month")["expense"].sum().to_dict()
        summary += f"Monthly expenses: {monthly}\n"
    if "weight" in cols:
        summary += f"Avg weight: {df['weight'].mean():.1f}\n"
    if "quantity" in cols and "price" in cols:
        summary += f"Inventory value: {(df['quantity']*df['price']).sum():.2f}\n"

    folder = f"data_storage/user_{user_id}/insights"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/insights.txt","w") as f: f.write(summary)
    return summary

def insights_coverage(df):
    cols = df.columns.tolist()
    coverage = []
    for category, metrics in INSIGHT_REGISTRY.items():
        for metric, required_cols in metrics.items():
            available = all(col in cols for col in required_cols)
            coverage.append({
                "category": category,
                "metric": metric,
                "required_cols": ", ".join(required_cols),
                "available": "✔ Available" if available else "✘ Missing"
            })
    return coverage

def show_insights():
    df = st.session_state.get("data")
    user = st.session_state.get("user")
    if df is None or not user:
        st.warning("Upload data first.")
        return
    summary = adaptive_insights(df, user["id"], user.get("industry","generic"))
    st.write(summary)

    st.subheader("Insights Coverage Report")
    coverage = insights_coverage(df)
    for item in coverage:
        st.write(f"- {item['metric']} ({item['category']}) → {item['available']} | Needs: {item['required_cols']}")