import streamlit as st
import plotly.express as px

def show_segmentation(df):
    st.title("🧩 Customer Segmentation")

    if "Segment" not in df.columns:
        st.error("❌ 'Segment' column not found. Please ensure segmentation has been applied to the dataset.")
        return

    # KPI: Number of segments
    st.metric("Number of Segments", df["Segment"].nunique())

    # Segment Distribution
    seg_counts = df["Segment"].value_counts()

    fig = px.pie(
        names=seg_counts.index,
        values=seg_counts.values,
        title="📊 Customer Segment Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Segment Characteristics
    st.subheader("📌 Segment Profiles")
    st.write(df.groupby("Segment").mean(numeric_only=True))
