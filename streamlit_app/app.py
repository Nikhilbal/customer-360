import streamlit as st
import pandas as pd
import os

import plotly.express as px

# Load data
@st.cache_data
def load_data():
    data_path = "data/final/customer360_final_dataset.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        st.error("❌ Data file not found: " + data_path)
        return pd.DataFrame()

df = load_data()

# Import pages
from pages.page_overview import show_overview
from pages.page_customer_explorer import show_customer_explorer
from pages.page_churn_analysis import show_churn_analysis
from pages.page_segmentation import show_segmentation
from pages.page_product_insights import show_product_insights
from pages.page_geography import show_geography
from pages.page_churn_prediction import show_churn_prediction



# Sidebar Navigation
st.sidebar.title("📊 Customer360 Dashboard")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Customer Explorer",
        "Churn Analysis",
        "Product Insights",
        "Geography",
    ]
)

# Page Router
if page == "Overview":
    show_overview(df)

elif page == "Customer Explorer":
    show_customer_explorer(df)

elif page == "Churn Analysis":
    show_churn_analysis(df)


elif page == "Segmentation":
    show_segmentation(df)

elif page == "Product Insights":
    show_product_insights(df)

elif page == "Geography":
    show_geography(df)

elif page == "Churn Prediction":
    show_churn_prediction(df)
