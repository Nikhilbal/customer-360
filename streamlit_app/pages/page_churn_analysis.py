# streamlit_app/pages/page_churn_analysis.py

import os, sys
import streamlit as st
import plotly.express as px
import pandas as pd

# Allow imports from main folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_data


def show_churn_analysis(df=None):

    st.title("📉 Customer Churn Analysis Dashboard")

    # Load data if not passed
    if df is None:
        df = load_data()

    if df is None or df.empty:
        st.warning("⚠ No data loaded.")
        return

    # Detect churn column automatically
    churn_candidates = [c for c in df.columns if "churn" in c.lower()]
    if not churn_candidates:
        st.error("❌ No churn column found (expected: churn_flag, churn, is_churn, etc.)")
        return

    churn_col = churn_candidates[0]  # first detected match

    # Normalize churn values (0/1 → Yes/No)
    if df[churn_col].dtype != "object":
        df[churn_col] = df[churn_col].map({1: "Yes", 0: "No"}).fillna("Unknown")

    # ------------------ Summary Metrics ------------------
    churn_rate = (df[churn_col].value_counts(normalize=True).get("Yes", 0)) * 100
    churned_count = df[churn_col].value_counts().get("Yes", 0)

    st.subheader("📌 Key Metrics Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Customers", f"{len(df):,}")
    col2.metric("🔥 Customers Churned", churned_count)
    col3.metric("📉 Churn Rate", f"{churn_rate:.2f}%")

    st.markdown("---")

    # ------------------ Churn Pie Chart ------------------
    st.subheader("📊 Churn Distribution")

    fig = px.pie(
        df,
        names=churn_col,
        title="Overall Churn Status",
        hole=0.45
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ------------------ Category Breakdown (Optional Fields) ------------------

    # Contract Type (optional)
    contract_col = next((c for c in df.columns if "contract" in c.lower()), None)

    if contract_col:
        st.subheader(f"📝 Churn by {contract_col.title()}")
        fig_contract = px.histogram(df, x=contract_col, color=churn_col,
                                    barmode="group",
                                    title=f"{contract_col.title()} vs Churn")
        st.plotly_chart(fig_contract, use_container_width=True)

    # Segment Type (optional)
    segment_col = next((c for c in df.columns if "segment" in c.lower()), None)

    if segment_col:
        st.subheader(f"📌 Churn by {segment_col.title()}")
        fig_segment = px.bar(
            df.groupby([segment_col, churn_col]).size().reset_index(name="count"),
            x=segment_col,
            y="count",
            color=churn_col,
            title="Segment Churn Breakdown"
        )
        st.plotly_chart(fig_segment, use_container_width=True)

    st.markdown("---")

    # ------------------ Churn Correlation ------------------
    st.subheader("📈 Factors Influencing Churn")

    numeric_df = df.select_dtypes(include=["int64", "float64"]).copy()

    if numeric_df.empty:
        st.warning("⚠ No numeric columns detected for correlation analysis.")
    else:

        # Add churn back in numeric form for correlation
        numeric_df["Churn_Numeric"] = df[churn_col].map({"Yes": 1, "No": 0})

        correlations = numeric_df.corr()["Churn_Numeric"].sort_values(ascending=False)
        st.dataframe(
            correlations.to_frame("Correlation with Churn")
            .style.background_gradient(cmap="coolwarm")
        )

    st.markdown("---")

    st.success("📌 Analysis complete — scroll up to explore insights!")
    st.info("💡 Higher churn means customers are leaving. Target retention strategies based on contracts, spending behavior, or customer segments.")


# Required entry function for Streamlit multipage app
def app():
    df = load_data()
    show_churn_analysis(df)
