# src/utils/tenants.py

import pandas as pd

def get_tenant_data(tenant_id: str, module: str) -> pd.DataFrame:
    """
    Return tenant-specific data for a given module.
    Replace demo data with actual DB queries filtered by tenant_id.
    """
    demo_data = {
        "analytics": {
            "tenant_A": pd.DataFrame({"Metric": ["Sales", "Growth"], "Value": [100, 20]}),
            "tenant_B": pd.DataFrame({"Metric": ["Sales", "Growth"], "Value": [50, 10]}),
            "global_admin": pd.DataFrame({"Tenant": ["A", "B"], "Sales": [100, 50], "Growth": [20, 10]}),
        },
        "data_pipeline": {
            "tenant_A": pd.DataFrame({"Step": ["Clean", "Transform"], "Status": ["Done", "Pending"]}),
            "tenant_B": pd.DataFrame({"Step": ["Clean"], "Status": ["Done"]}),
            "global_admin": pd.DataFrame({"Tenant": ["A", "B"], "Pipelines": [2, 1]}),
        },
        "inventory": {
            "tenant_A": pd.DataFrame({"Item": ["Widget A", "Widget B"], "Stock": [20, 5]}),
            "tenant_B": pd.DataFrame({"Item": ["Widget C"], "Stock": [10]}),
            "global_admin": pd.DataFrame({"Tenant": ["A", "B"], "Total Stock": [25, 10]}),
        },
        "reporting": {
            "tenant_A": pd.DataFrame({"Report": ["Monthly"], "Status": ["Generated"]}),
            "tenant_B": pd.DataFrame({"Report": ["Monthly"], "Status": ["Pending"]}),
            "global_admin": pd.DataFrame({"Tenant": ["A", "B"], "Reports": [1, 1]}),
        },
        "copilot": {
            "tenant_A": pd.DataFrame({"Suggestion": ["Add more sales columns"]}),
            "tenant_B": pd.DataFrame({"Suggestion": ["Track inventory turnover"]}),
            "global_admin": pd.DataFrame({"Tenant": ["A", "B"], "Suggestions": [1, 1]}),
        }
    }

    return demo_data.get(module, {}).get(tenant_id, pd.DataFrame())
