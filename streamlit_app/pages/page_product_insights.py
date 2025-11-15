# streamlit_app/pages/page_product_insights.py

import os, sys
import streamlit as st
import plotly.express as px

# Allow imports from main directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_data


def show_product_insights(df=None):

    st.title("🛍 Product Insights Dashboard")

    # Load data if not passed
    if df is None:
        df = load_data()

    if df is None or df.empty:
        st.error("❌ No data available for product analysis.")
        return

    # Detect columns automatically
    product_col = next((col for col in df.columns if "product" in col.lower() and "category" not in col.lower()), None)
    category_col = next((col for col in df.columns if "category" in col.lower()), None)

    spend_col = next(
        (col for col in df.columns if "total_spent" in col.lower() or "price" in col.lower() or "value" in col.lower()),
        None
    )

    qty_col = next((col for col in df.columns if "qty" in col.lower() or "quantity" in col.lower()), None)

    if spend_col is None:
        st.error("⚠ No spending column detected in dataset. Cannot generate revenue charts.")
        return

    st.write("---")

    # ===========================
    # 🔥 Top Product Categories
    # ===========================
    if category_col:
        st.subheader("🏆 Top Product Categories by Revenue")

        category_df = (
            df.groupby(category_col)[spend_col]
            .sum()
            .reset_index()
            .sort_values(spend_col, ascending=False)
            .head(15)
        )

        fig_cat = px.bar(
            category_df,
            x=category_col,
            y=spend_col,
            title="Top Selling Categories by Revenue",
            text_auto=True
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    else:
        st.warning("⚠ No product category column found.")

    st.write("---")

    # ===========================
    # ⭐ Best Selling Individual Products
    # ===========================
    if product_col:
        st.subheader("⭐ Top Products by Total Sales")

        product_df = (
            df.groupby(product_col)[spend_col]
            .sum()
            .reset_index()
            .sort_values(spend_col, ascending=False)
            .head(15)
        )

        fig_prod = px.bar(
            product_df, 
            x=product_col, 
            y=spend_col,
            title="Top Revenue Generating Products",
            text_auto=True
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    st.write("---")

    # ===========================
    # 📦 Best Selling Products by Quantity (Optional)
    # ===========================
    if qty_col and product_col:
        st.subheader("📦 Best Selling Products by Quantity")

        qty_df = (
            df.groupby(product_col)[qty_col]
            .sum()
            .reset_index()
            .sort_values(qty_col, ascending=False)
            .head(15)
        )

        fig_qty = px.bar(
            qty_df,
            x=product_col,
            y=qty_col,
            title="Top Products by Units Sold",
            text_auto=True
        )
        st.plotly_chart(fig_qty, use_container_width=True)

    else:
        st.info("ℹ Quantity column not found — skipping sales volume ranking.")


    st.success("🎯 Product insights loaded successfully!")
