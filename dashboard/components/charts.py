"""
charts.py
---------
Author: Tony Ngo

Description:
    This module provides reusable chart functions for the VTA Transit
    Analytics dashboard. These charts are imported into app.py or other
    dashboard components for visual analysis.

This program:
    Defines modular functions that create and return matplotlib figures
    for key metrics such as:
        - Predicted vs Actual Delay
        - Feature Importance
        - Delay Distribution
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def predicted_vs_actual_chart(y_true, y_pred):
    """
    Creates a scatterplot comparing actual vs predicted delay values.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_true, y_pred, alpha=0.5, edgecolor="k")
    ax.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "r--", lw=2)
    ax.set_xlabel("Actual Delay (minutes)")
    ax.set_ylabel("Predicted Delay (minutes)")
    ax.set_title("Predicted vs Actual Delay Times")
    plt.tight_layout()
    return fig

def feature_importance_chart(model, feature_names, top_n=10):
    """
    Creates a horizontal bar chart showing top N important features.
    Works with models that have feature_importances_ attribute.
    """
    if not hasattr(model, "feature_importances_"):
        raise ValueError("This model does not support feature importance visualization.")

    importance = model.feature_importances_
    sorted_idx = np.argsort(importance)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(np.array(feature_names)[sorted_idx][::-1], importance[sorted_idx][::-1])
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.set_title(f"Top {top_n} Most Important Features")
    plt.tight_layout()
    return fig

def delay_distribution_chart(df):
    """
    Creates a histogram showing distribution of delay_minutes.
    """
    if "delay_minutes" not in df.columns:
        raise KeyError("The dataset must include a 'delay_minutes' column.")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(df["delay_minutes"].dropna(), bins=30, color="skyblue", edgecolor="black")
    ax.set_xlabel("Delay (minutes)")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Distribution of Transit Delays")
    plt.tight_layout()
    return fig

