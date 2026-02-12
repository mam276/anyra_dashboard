import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_retention_model(df, user_id):
    if "churn" not in df:
        return None, "No churn data available."
    X = df.drop(columns=["churn"])
    y = df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train,y_train)
    folder = f"data_storage/user_{user_id}/models"
    os.makedirs(folder, exist_ok=True)
    joblib.dump(model, f"{folder}/retention_model.pkl")
    return model, f"Accuracy: {model.score(X_test,y_test):.2f}"

def predict_churn(df, user_id):
    model_path = f"data_storage/user_{user_id}/models/retention_model.pkl"
    if not os.path.exists(model_path):
        return None
    model = joblib.load(model_path)
    df["churn_risk"] = model.predict_proba(df.drop(columns=["churn"]))[:,1]
    folder = f"data_storage/user_{user_id}/analytics"
    os.makedirs(folder, exist_ok=True)
    df.to_csv(f"{folder}/churn_predictions.csv", index=False)
    return df[["customer_id","churn_risk"]]