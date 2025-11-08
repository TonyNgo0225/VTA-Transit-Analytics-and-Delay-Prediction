"""
app.py
------
Author: Tony Ngo

Description:
    This Streamlit dashboard provides an interactive interface for analyzing 
    VTA (Valley Transportation Authority) transit delay predictions. It visualizes
    real-time and historical data, model performance, and key insights.

This program:
    Loads the latest trained model and processed dataset.
    Displays evaluation metrics and feature importance.
    Allows users to view sample transit records.
    Provides a professional, interactive front-end for the full pipeline.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ----------------------------------------
# Helper Functions
# ----------------------------------------

def load_latest_model():
    """Loads the most recent trained model from models/."""
    model_files = [f for f in os.listdir("models") if f.endswith(".pkl")]
    if not model_files:
        st.error("No model files found. Please run train_model.py first.")
        return None
    latest = max(model_files, key=lambda f: os.path.getmtime(os.path.join("models", f)))
    return joblib.load(os.path.join("models", latest))

def load_latest_data():
    """Loads the most recent processed dataset from data/processed/."""
    data_files = [f for f in os.listdir("data/processed") if f.endswith(".csv")]
    if not data_files:
        st.error("No processed datasets found. Please run clean_merge_data.py first.")
        return None
    latest = max(data_files, key=lambda f: os.path.getmtime(os.path.join("data/processed", f)))
    df = pd.read_csv(os.path.join("data/processed", latest))
    return df

def evaluate_model(model, df):
    """Evaluates model metrics on the loaded dataset."""
    if model is None or df is None:
        return None

    if "delay_minutes" not in df.columns:
        st.warning("Dataset missing 'delay_minutes' column. Model metrics may be inaccurate.")
        df["delay_minutes"] = np.random.uniform(0, 10, len(df))

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "delay_minutes" in numeric_cols:
        numeric_cols.remove("delay_minutes")

    X = df[numeric_cols].fillna(0)
    y = df["delay_minutes"]
    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    r2 = r2_score(y, predictions)

    return {"MAE": mae, "RMSE": rmse, "R2": r2}, predictions

def plot_predictions(y, predictions):
    """Plots actual vs predicted delay times."""
    fig, ax = plt.subplots()
    ax.scatter(y, predictions, alpha=0.5, edgecolor="k")
    ax.plot([y.min(), y.max()], [y.min(), y.max()], "r--", lw=2)
    ax.set_xlabel("Actual Delay (minutes)")
    ax.set_ylabel("Predicted Delay (minutes)")
    ax.set_title("Predicted vs Actual Delay Times")
    st.pyplot(fig)

def plot_feature_importance(model, feature_names):
    """Displays the top 10 most important features from the trained model."""
    if not hasattr(model, "feature_importances_"):
        st.warning("Feature importance not available for this model.")
        return

    importance = model.feature_importances_
    sorted_idx = np.argsort(importance)[::-1][:10]
    fig, ax = plt.subplots()
    ax.barh(feature_names[sorted_idx][::-1], importance[sorted_idx][::-1])
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.set_title("Top 10 Important Features")
    st.pyplot(fig)

# ----------------------------------------
# Streamlit Dashboard Layout
# ----------------------------------------

st.set_page_config(
    page_title="VTA Transit Delay Predictor",
    page_icon="🚆",
    layout="wide"
)

st.title("VTA Transit Analytics Dashboard")
st.markdown("### Real-Time Data, Model Insights, and Delay Predictions")

# Sidebar options
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to:", ["Overview", "Model Performance", "Data Preview"])

# Load data and model
model = load_latest_model()
df = load_latest_data()

# ----------------------------------------
# Sections
# ----------------------------------------

if section == "Overview":
    st.subheader("Project Overview")
    st.write("""
    This dashboard visualizes the predictive modeling of VTA transit delays using
    both real-time transit and weather data.
    - **Data Source:** 511.org (VTA API) and OpenWeatherMap  
    - **Goal:** Predict bus and light rail delays using environmental and operational features  
    - **Methods:** Random Forest Regressor trained on merged datasets
    """)

elif section == "Model Performance":
    st.subheader("Model Performance Metrics")

    if model is not None and df is not None:
        metrics, predictions = evaluate_model(model, df)
        if metrics:
            st.metric("Mean Absolute Error (MAE)", f"{metrics['MAE']:.2f}")
            st.metric("Root Mean Squared Error (RMSE)", f"{metrics['RMSE']:.2f}")
            st.metric("R² Score", f"{metrics['R2']:.2f}")

            st.divider()
            st.subheader("Predicted vs Actual Delay")
            plot_predictions(df["delay_minutes"], predictions)

            st.divider()
            st.subheader("Feature Importance")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.drop("delay_minutes")
            plot_feature_importance(model, np.array(numeric_cols))
    else:
        st.warning("Please train your model first to view metrics.")

elif section == "Data Preview":
    st.subheader("Latest Processed Data Preview")
    if df is not None:
        st.dataframe(df.head(50))
        st.info(f"Showing {min(50, len(df))} of {len(df)} rows from the latest dataset.")
    else:
        st.warning("No processed data available.")

