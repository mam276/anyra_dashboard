def retention_kpis(df):
    kpis = {}
    if "customer_id" in df:
        kpis["total_customers"] = df["customer_id"].nunique()
    if "churn" in df:
        kpis["churn_rate"] = df["churn"].mean() * 100
    if "repeat_purchase" in df:
        kpis["repeat_purchase_rate"] = df["repeat_purchase"].mean() * 100
    if "lifetime_value" in df:
        kpis["avg_clv"] = df["lifetime_value"].mean()
    return kpis