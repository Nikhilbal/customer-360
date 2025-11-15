# streamlit_app/pages/page_customer_explorer.py

import os, sys
import streamlit as st
import plotly.express as px
import pandas as pd

# Allow imports from main folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_data


def show_customer_explorer(df=None):

    st.title("🔍 Customer Explorer")

    # Load data if not passed
    if df is None:
        df = load_data()

    if df is None or df.empty:
        st.error("❌ No data available for customer exploration.")
        return

    # Detect key columns dynamically
    customer_col = next((col for col in df.columns if "customer" in col.lower()), None)
    spend_col = next((col for col in df.columns if "spent" in col.lower()), None)
    product_col = next((col for col in df.columns if "product" in col.lower() and "category" not in col.lower()), None)
    date_col = next((col for col in df.columns if "date" in col.lower() or "purchase" in col.lower()), None)

    if not customer_col:
        st.error("⚠ No customer ID column detected.")
        return

    st.write("Search and explore individual customer purchase behavior and insights.")
    st.write("---")

    # Customer Selection Filter
    selected_customer = st.selectbox("Select Customer", sorted(df[customer_col].unique()))

    cust_data = df[df[customer_col] == selected_customer]

    if cust_data.empty:
        st.warning("⚠ No records found for this customer.")
        return

    # -------------------- Customer Summary Metrics --------------------
    st.subheader("📌 Customer Summary")

    total_orders = len(cust_data)
    total_spend = cust_data[spend_col].sum() if spend_col else None
    last_purchase = (
        pd.to_datetime(cust_data[date_col]).max().strftime("%d %b %Y")
        if date_col else "Not Available"
    )
    segments = ", ".join(cust_data["segment_name"].unique()) if "segment_name" in cust_data.columns else "Unknown"
    churn_value = cust_data["churn_flag"].iloc[0] if "churn_flag" in cust_data.columns else None

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛍 Total Orders", total_orders)
    col2.metric("💰 Total Spend", f"₹{total_spend:,.0f}" if total_spend else "N/A")
    col3.metric("📅 Last Purchase", last_purchase)
    col4.metric("📌 Segment", segments)

    if churn_value is not None:
        st.warning("⚠ Customer is at *risk of churn*" if churn_value == 1 else "✅ Customer is active")

    st.write("---")

    # -------------------- Transaction Table --------------------
    st.subheader("🧾 Purchase History")

    display_cols = [c for c in [date_col, product_col, spend_col, "product_category_name", "order_id"] if c in cust_data.columns]

    st.dataframe(cust_data[display_cols].sort_values(date_col, ascending=False), use_container_width=True)

    # -------------------- Visualization: Trend --------------------
    if date_col and spend_col:
        trend_df = cust_data.copy()
        trend_df[date_col] = pd.to_datetime(trend_df[date_col])

        fig = px.line(
            trend_df.sort_values(date_col),
            x=date_col, y=spend_col,
            title="📈 Spend Trend Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------- Visualization: Product Spend --------------------
    if product_col and spend_col:
        product_summary = (
            cust_data.groupby(product_col)[spend_col]
            .sum()
            .reset_index()
            .sort_values(spend_col, ascending=False)
        )

        st.subheader("🛒 Spend by Product")

        fig2 = px.bar(
            product_summary,
            x=product_col, y=spend_col,
            title="Spend Breakdown by Product",
            text_auto=True
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.success("🎯 Customer profile loaded successfully!")

