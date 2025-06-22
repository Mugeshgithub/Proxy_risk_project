import streamlit as st
import pandas as pd
from analysis import (
    load_and_preprocess,
    generate_fraud_score_chart,
    generate_country_chart,
    generate_isp_chart,
    generate_geographic_heatmap
)

# Set page configuration
st.set_page_config(layout="wide", page_title="Proxy Risk Analysis Dashboard")

# --- App Title and Description ---
st.title("Proxy Service Risk Analysis Dashboard")
st.markdown("""
This dashboard provides an analysis of proxy services, highlighting potential risks based on fraud scores, geographic location, and Internet Service Providers (ISPs).
Use the insights from these charts to inform your security policies and mitigate risks.
""")

# --- Load Data ---
@st.cache_data
def load_data():
    df = load_and_preprocess('PROXYSCOPEW.csv')
    return df

proxy_df = load_data()

if proxy_df is not None:
    # --- Display Charts ---
    st.header("High-Risk Proxy Analysis")

    # Row 1: Fraud Score and Country Distribution
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution by Fraud Score")
        fig_fraud = generate_fraud_score_chart(proxy_df)
        st.plotly_chart(fig_fraud, use_container_width=True)

    with col2:
        st.subheader("Top 10 High-Risk Countries")
        fig_country = generate_country_chart(proxy_df)
        st.plotly_chart(fig_country, use_container_width=True)

    # Row 2: ISP Distribution and Geographic Heatmap
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Top 5 High-Risk ISPs")
        fig_isp = generate_isp_chart(proxy_df)
        st.plotly_chart(fig_isp, use_container_width=True)

    with col4:
        st.subheader("Geographic Heatmap of High-Risk Proxies")
        fig_heatmap = generate_geographic_heatmap(proxy_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)

else:
    st.error("Could not load and process the data. Please check the data file 'PROXYSCOPEW.csv'.") 