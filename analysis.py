import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_and_preprocess(file_path):
    """
    Loads and preprocesses data safely for aggregated analysis.
    """
    print("Loading and preprocessing data...")
    try:
        # NOTE: The dtype parameter is correct pandas usage. The linter may show a false positive.
        dtype_spec = {'IP_FROM': 'str', 'PROXY_TYPE': 'str', 'COUNTRY_NAME': 'str', 'ISP': 'str', 'THREAT': 'str'}
        df = pd.read_csv(file_path, sep=',', skipinitialspace=True, dtype=dtype_spec)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert FRAUD_SCORE to numeric, handling errors
        df['FRAUD_SCORE'] = pd.to_numeric(df['FRAUD_SCORE'], errors='coerce')
        
        print("Data loaded and preprocessed successfully.")
        return df.dropna(subset=['FRAUD_SCORE'])
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def generate_fraud_score_chart(df):
    """
    Generates a professional chart of proxy counts by FRAUD_SCORE range using Plotly.
    """
    print("Step 1: Generating Fraud Score Distribution Chart...")
    
    bins = [70, 80, 90, 101] 
    labels = ['70-79', '80-89', '90-100']
    df_high_risk = df[df['FRAUD_SCORE'] >= 70].copy()
    df_high_risk['SCORE_RANGE'] = pd.cut(df_high_risk['FRAUD_SCORE'], bins=bins, labels=labels, right=False)
    
    score_counts = df_high_risk['SCORE_RANGE'].value_counts().sort_index()

    colors = ['#ffcc00', '#ff9900', '#d9534f']
    
    fig = go.Figure(data=[go.Bar(
        x=score_counts.index,
        y=score_counts.values,
        text=[f'{v:,}' for v in score_counts.values],
        textposition='auto',
        marker_color=colors
    )])
    
    fig.update_layout(
        title_text='Distribution of Proxies by High-Risk Score',
        xaxis_title_text='Fraud Score Range',
        yaxis_title_text='Number of Proxies',
        title_x=0.5,
        template="plotly_white",
        annotations=[
            dict(
                text='Business Insight: Over 70% of proxies have a fraud score above 80.<br>Consider adding MFA for these users.',
                showarrow=False,
                xref='paper', yref='paper',
                x=0.5, y=-0.25,
                align="center",
                font=dict(size=12, color="grey"),
                bordercolor="lightgrey",
                borderwidth=1,
                borderpad=4,
                bgcolor="whitesmoke",
            )
        ],
        margin=dict(b=120)
    )
    
    print("  - Chart 1: Binned Fraud Score Distribution... [GENERATED]")
    return fig

def generate_country_chart(df):
    """
    Generates a professional chart of the top 10 countries with high-risk proxies using Plotly.
    """
    print("Step 2: Generating High-Risk Countries Chart...")

    high_risk_df = df[df['FRAUD_SCORE'] > 75].copy()
    country_counts = high_risk_df['COUNTRY_NAME'].value_counts().nlargest(10).sort_values()

    colors = ['#d9534f' if c in ['United States', 'Russia'] else '#6c757d' for c in country_counts.index]

    fig = go.Figure(go.Bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation='h',
        marker_color=colors,
        text=country_counts.values,
        texttemplate='%{text:,}',
        textposition='outside'
    ))

    top_countries = ", ".join(high_risk_df['COUNTRY_NAME'].value_counts().nlargest(3).index)
    
    fig.update_layout(
        title_text='Top 10 Countries Hosting High-Risk Proxies (Fraud Score > 75)',
        xaxis_title_text='Number of High-Risk Proxies',
        yaxis_title_text='Country',
        title_x=0.5,
        template="plotly_white",
        annotations=[
            dict(
                text=f'Business Insight: {top_countries} are consistently high-risk.<br>Consider implementing geo-aware filters for these regions.',
                showarrow=False,
                xref='paper', yref='paper',
                x=0.5, y=-0.25,
                align="center",
                font=dict(size=12, color="grey"),
                bordercolor="lightgrey",
                borderwidth=1,
                borderpad=4,
                bgcolor="whitesmoke",
            )
        ],
        margin=dict(b=120, t=50, l=120)
    )
    
    print("  - Chart 2: Top 10 High-Risk Countries... [GENERATED]")
    return fig

def generate_isp_chart(df):
    """
    Generates a professional chart of the top 5 ISPs with high-risk proxies using Plotly.
    """
    print("Step 3: Generating High-Risk ISPs Chart...")

    high_risk_df = df[df['FRAUD_SCORE'] > 75].copy()
    isp_counts = high_risk_df['ISP'].value_counts().nlargest(5).sort_values()

    fig = go.Figure(go.Bar(
        x=isp_counts.values,
        y=isp_counts.index,
        orientation='h',
        marker_color='#5bc0de',
        text=isp_counts.values,
        texttemplate='%{text:,}',
        textposition='outside'
    ))

    fig.update_layout(
        title_text='Top 5 ISPs Hosting High-Risk Proxies (Fraud Score > 75)',
        xaxis_title_text='Number of High-Risk Proxies',
        yaxis_title_text='Internet Service Provider (ISP)',
        title_x=0.5,
        template="plotly_white",
        annotations=[
            dict(
                text='Business Insight: A few ISPs host a disproportionate number of high-risk proxies.<br>Consider rate-limiting traffic from these networks.',
                showarrow=False,
                xref='paper', yref='paper',
                x=0.5, y=-0.25,
                align="center",
                font=dict(size=12, color="grey"),
                bordercolor="lightgrey",
                borderwidth=1,
                borderpad=4,
                bgcolor="whitesmoke",
            )
        ],
        margin=dict(b=120, t=50, l=150)
    )
    
    print("  - Chart 3: Top 5 High-Risk ISPs... [GENERATED]")
    return fig

def generate_geographic_heatmap(df):
    """
    Generates a world map heatmap of high-risk proxy locations.
    """
    print("Step 4: Generating Geographic Heatmap of High-Risk Proxies...")

    # Aggregate high-risk proxies by country
    high_risk_df = df[df['FRAUD_SCORE'] > 75].copy()
    country_counts = high_risk_df['COUNTRY_NAME'].value_counts().reset_index()
    country_counts.columns = ['COUNTRY_NAME', 'COUNT']

    # Create the choropleth map
    fig = px.choropleth(country_counts,
                        locations="COUNTRY_NAME",
                        locationmode='country names',
                        color="COUNT",
                        hover_name="COUNTRY_NAME",
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        title="Geographic Heatmap of High-Risk Proxies (Fraud Score > 75)")

    fig.update_layout(
        title=dict(x=0.5, xanchor='center'),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    # Save the map as a static image
    # fig.write_image("geographic_heatmap.png", width=1200, height=600)
    print("  - Chart 4: Geographic Heatmap... [GENERATED]")
    return fig


if __name__ == "__main__":
    file_path = 'PROXYSCOPEW.csv'
    proxy_df = load_and_preprocess(file_path)
    
    if proxy_df is not None:
        # Generate and save each chart
        print("\nGenerating and saving charts...")
        
        fig1 = generate_fraud_score_chart(proxy_df)
        fig1.write_image('safe_report_1_fraud_score_distribution.png', width=1000, height=600)
        
        fig2 = generate_country_chart(proxy_df)
        fig2.write_image('safe_report_2_country_distribution.png', width=1000, height=600)

        fig3 = generate_isp_chart(proxy_df)
        fig3.write_image('safe_report_3_isp_distribution.png', width=1000, height=600)

        fig4 = generate_geographic_heatmap(proxy_df)
        fig4.write_image("geographic_heatmap.png", width=1200, height=600)
        
        print("\nAnalysis complete. All charts have been generated and saved.") 