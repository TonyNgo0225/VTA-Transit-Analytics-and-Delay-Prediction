"""
evaluate_model.py
-----------------
Author: Tony Ngo

Description:
    This script evaluates the trained machine learning model used to predict
    VTA transit delays. It loads the most recent trained model and dataset,
    calculates key performance metrics, and visualizes results.

This program:
    Loads the most recent model and processed dataset.
    Evaluates the model using test data (MAE, RMSE, R²).
    Displays feature importance and prediction vs. actual plots.
    Saves charts to the "reports/figures" folder.

    These results help understand how accurately the model predicts delays
    and which variables (like temperature, humidity, or route) influence them most.
"""

import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from datetime import datetime

# Create folder for saving visual reports
os.makedirs("reports/figures", exist_ok=True)

def load_latest_model():
    """
    Loads the most recently saved trained model from the models/ folder.
    """
    model_files = [f for f in os.listdir("models") if f.endswith(".pkl")]
    if not model_files:
        raise FileNotFoundError("No model files found in 'models/'. Train a model first.")
    latest_model = max(model_files, key=lambda x: os.path.getmtime(os.path.join("models", x)))
    print(f"Loading model: {latest_model}")
    return joblib.load(os.path.join("models", latest_model))

def load_processed_data():
    """
    Loads the most recent processed dataset for evaluation.
    """
    processed_files = [f for f in os.listdir("data/processed") if f.endswith(".csv")]
    if not processed_files:
        raise FileNotFoundError("No processed data found in 'data/processed/'.")
    latest_data = max(processed_files, key=lambda x: os.path.getmtime(os.path.join("data/processed", x)))
    print(f"Loading dataset: {latest_data}")
    df = pd.read_csv(os.path.join("data/processed", latest_data))
    return df

def evaluate_model(model, df):
    """
    Evaluates model performance using numeric features from the dataset.
    """
    print("Evaluating model performance...")
    if "delay_minutes" not in df.columns:
        raise ValueError("Dataset missing 'delay_minutes' column. Add delay data before evaluating.")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col != "delay_minutes"]

    X = df[numeric_cols].fillna(0)
    y = df["delay_minutes"]
    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    r2 = r2_score(y, predictions)

    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R²: {r2:.3f}")

    metrics = {"MAE": mae, "RMSE": rmse, "R2": r2}
    return predictions, metrics

def plot_results(y, predictions):
    """
    Generates plots comparing actual vs predicted delay times.
    """
    plt.figure(figsize=(7, 7))
    plt.scatter(y, predictions, alpha=0.5, edgecolor="k")
    plt.xlabel("Actual Delay (minutes)")
    plt.ylabel("Predicted Delay (minutes)")
    plt.title("Predicted vs Actual Delay Times")
    plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--")
    plt.tight_layout()
    filename = f"reports/figures/predicted_vs_actual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    print(f"Saved predicted vs actual plot as {filename}")
    plt.close()

def plot_feature_importance(model, feature_names):
    """
    Plots feature importance for Random Forest or similar models.
    """
    if not hasattr(model, "feature_importances_"):
        print("Model does not support feature importance.")
        return

    importance = model.feature_importances_
    sorted_idx = np.argsort(importance)[::-1]
    top_features = feature_names[sorted_idx][:10]
    top_importance = importance[sorted_idx][:10]

    plt.figure(figsize=(8, 5))
    plt.barh(top_features[::-1], top_importance[::-1])
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("Top 10 Most Important Features")
    plt.tight_layout()
    filename = f"reports/figures/feature_importance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    print(f"Saved feature importance plot as {filename}")
    plt.close()

if __name__ == "__main__":
    try:
        model = load_latest_model()
        df = load_processed_data()
        predictions, metrics = evaluate_model(model, df)
        plot_results(df["delay_minutes"], predictions)
        feature_names = df.select_dtypes(include=[np.number]).columns.drop("delay_minutes")
        plot_feature_importance(model, feature_names)
        print("Model evaluation complete.")
    except Exception as e:
        print(f"Error during model evaluation: {e}")
