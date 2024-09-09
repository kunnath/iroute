import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Constants
num_records = 10

# Sample Data
df = pd.DataFrame({
    'timestamp': pd.date_range(start='2022-01-01', periods=10, freq='D'),
    'speed': [60, 62, 63, 59, 58, 57, 61, 64, 60, 62],
    'fuel_consumption': [8, 7.8, 7.9, 8.1, 7.7, 8.2, 8.0, 7.9, 7.8, 8.1],
    'engine_temp': [90, 91, 89, 92, 88, 87, 90, 91, 89, 90],
    'event': ['Speeding', 'Harsh Braking', 'Normal', 'Speeding', 'Normal', 'Speeding', 'Normal', 'Harsh Braking','Speeding', 'Normal'],
    'latitude': [37.77, 37.78, 37.76, 37.77, 37.79, 37.80, 37.77, 37.76, 37.75, 37.78],
    'longitude': [-122.41, -122.42, -122.43, -122.44, -122.40, -122.39, -122.41, -122.42, -122.43, -122.44],
    'driver_id': np.random.randint(1, 101, num_records),
    'profile': np.random.choice(['Safe', 'Risky', 'Aggressive'], num_records),
    'driving_pattern': np.random.choice(['City', 'Highway', 'Mixed'], num_records),
    'severity_factor': np.random.uniform(0, 1, num_records),
    'cluster_risk': np.random.uniform(0, 1, num_records),
    'research_data': np.random.uniform(0, 1, num_records),
    'weighted_risk': np.random.uniform(0, 1, num_records)
})

# Calculate correlations (dummy example)
df['correlation'] = df[['severity_factor', 'cluster_risk', 'research_data', 'weighted_risk']].corr().mean().mean()

# Streamlit App Layout
st.title('iroute Fleet Management Dashboard')

# Key Metrics
st.subheader('Key Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Resilient Driver", "0.8%")
col2.metric("Insurance Driving", "0.27%")
col3.metric("Safe Driving", "25.1%")
col4.metric("Computer Scoring", "45%")

# Driving Scores
st.subheader('Driving Scores')
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        names=['Tactical Driving', 'Technical Driving'],
        values=[60, 40],
        title='Professional Driving Score'
    )
    st.plotly_chart(fig1)

with col2:
    fig2 = px.pie(
        names=['Speed', 'Acceleration', 'Braking'],
        values=[40, 30, 30],
        title='Tactical Driving Score'
    )
    st.plotly_chart(fig2)

# Interactive Event Log (Map)
st.subheader('Interactive Event Log')
fig_map = px.scatter_mapbox(
    df,
    lat='latitude',
    lon='longitude',
    color='event',
    hover_data={'latitude': False, 'longitude': False, 'timestamp': True, 'speed': True},
    zoom=10,
    height=300
)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map)

# Risk Assessment and Prediction
st.subheader('Risk Assessment and Prediction')
st.write('''
- **Driver Profile Determination**
- **Driving Patterns Identification**
- **Severity Factor Calculation**
- **Cluster Risk Calculation**
- **Research Data Aggregation**
- **Weighted Risk Factor**
''')

# Strongest Correlations
st.subheader('Strongest Correlations')
st.dataframe(df)

# Daily Records (Bar Chart)
st.subheader('Daily Records')
fig_bar = px.bar(df, x='timestamp', y='speed', title='Daily Records')
st.plotly_chart(fig_bar)