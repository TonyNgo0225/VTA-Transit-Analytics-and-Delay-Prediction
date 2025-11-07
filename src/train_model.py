"""
train_model.py
---------------
Author: Tony Ngo

Description:
    This script trains a machine learning model to predict VTA transit delays 
    using the cleaned and merged dataset that includes both transit and weather data.

This program:
    Loads the most recent processed dataset from the "data/processed" folder.
    Splits the data into training and testing sets.
    Trains a Random Forest model using scikit-learn.
    Evaluates model performance using MAE, RMSE, and R² metrics.
    Saves the trained model and evaluation metrics to the "models" folder.

    The trained model will later be used for real-time delay predictions and 
    displayed in the dashboard visualization.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Create models directory if it doesn’t exist
os.makedirs("models", exist_ok=True)

def load_processed_data():
    """
    Loads the most recent processed dataset from the data/processed folder.
    """
    folder_path = "data/processed"
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No processed dataset found in data/processed/. Run clean_merge_data.py first.")
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    print(f"Loading dataset: {latest_file}")
    df = pd.read_csv(os.path.join(folder_path, latest_file))
    return df

def prepare_data(df):
    """
    Prepares the dataset for model training.
    Splits into features (X) and target (y). If 'delay_minutes' does not exist,
    a placeholder column is created for demonstration purposes.
    """
    print("Preparing data for training...")

    if "delay_minutes" not in df.columns:
        # Placeholder target column for initial testing
        df["delay_minutes"] = np.random.uniform(0, 10, size=len(df))

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "delay_minutes" in numeric_cols:
        numeric_cols.remove("delay_minutes")

    X = df[numeric_cols].fillna(0)
    y = df["delay_minutes"]

    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """
    Trains a Random Forest Regressor model to predict delay times.
    """
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model using standard regression metrics.
    Returns a dictionary of evaluation results.
    """
    print("Evaluating model performance...")
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R²: {r2:.3f}")

    return metrics

def save_model(model, metrics):
    """
    Saves the trained model and metrics into the models/ folder.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"models/delay_predictor_{timestamp}.pkl"
    metrics_filename = f"models/model_metrics_{timestamp}.csv"

    joblib.dump(model, model_filename)
    pd.Series(metrics).to_csv(metrics_filename)

    print(f"Model saved to {model_filename}")
    print(f"Metrics saved to {metrics_filename}")

if __name__ == "__main__":
    try:
        df = load_processed_data()
        X_train, X_test, y_train, y_test = prepare_data(df)
        model = train_model(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)
        save_model(model, metrics)
        print("Model training and saving complete.")
    except Exception as e:
        print(f"Error during model training: {e}")

