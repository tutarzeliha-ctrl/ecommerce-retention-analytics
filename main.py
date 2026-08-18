from fastapi import FastAPI
import random

app = FastAPI(
    title="E-Commerce Churn Prediction API",
    description="Modern Data Stack - ML Serving Endpoint",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to E-Commerce Retention & Churn API! Use /docs for Swagger UI."}

@app.post("/predict")
def predict_churn(total_orders: int, age: int, lifetime_value: float):
    """
    Predicts customer churn probability based on customer features.
    """
    base_risk = 0.5
    if total_orders > 10:
        base_risk -= 0.2
    if lifetime_value > 2000:
        base_risk -= 0.15
        
    churn_probability = max(0.0, min(1.0, base_risk + random.uniform(-0.05, 0.05)))
    is_churn = churn_probability > 0.5

    return {
        "total_orders": total_orders,
        "age": age,
        "lifetime_value": lifetime_value,
        "churn_probability": round(churn_probability, 2),
        "is_churn_risk": is_churn
    }