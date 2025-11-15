# streamlit_app/pages/page_geography.py

import os, sys
import streamlit as st
import plotly.express as px

# Allow utils import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_data


def show_geography(df=None):

    st.title("🌍 Geography Insights")

    # Load data if not passed
    if df is None:
        df = load_data()

    if df is None or df.empty:
        st.error("❌ No data available for geographic analysis.")
        return

    # Detect geography columns dynamically
    state_col = next((col for col in df.columns if "state" in col.lower()), None)
    city_col = next((col for col in df.columns if "city" in col.lower()), None)
    country_col = next((col for col in df.columns if "country" in col.lower()), None)

    # Detect spend column
    spend_col = next(
        (col for col in df.columns if "spent" in col.lower() or "value" in col.lower() or "price" in col.lower()),
        None
    )

    if spend_col is None:
        st.error("❌ Could not detect spending column in dataset.")
        return

    st.write("---")

    # ========== COUNTRIES ==========
    if country_col:
        st.subheader("🌐 Revenue by Country")

        country_df = df.groupby(country_col)[spend_col].sum().reset_index().sort_values(spend_col, ascending=False)

        fig = px.choropleth(
            country_df,
            locations=country_col,
            locationmode="country names",
            color=spend_col,
            title="Revenue Distribution by Country",
            hover_name=country_col
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

    # ========== STATES ==========
    if state_col:
        st.subheader("🏛 Revenue by State")

        state_df = df.groupby(state_col)[spend_col].sum().reset_index().sort_values(spend_col, ascending=False)

        fig = px.bar(
            state_df.head(20),
            x=state_col, y=spend_col,
            title="Top States by Revenue"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

    # ========== CITIES (Fallback if no state/country) ==========
    if city_col:
        st.subheader("🏙 Top Revenue Cities")

        city_df = df.groupby(city_col)[spend_col].sum().reset_index().sort_values(spend_col, ascending=False)

        fig = px.bar(
            city_df.head(20),
            x=city_col, y=spend_col,
            title="Top 20 Cities by Revenue"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠ No geographic columns found (city/state/country).")


