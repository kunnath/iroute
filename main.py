import dash
from dash import dcc, html
import dash_table
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('risk_assessment_data.csv')

# Initialize the app
app = dash.Dash(__name__)
app.title = "iroute Fleet Management Dashboard"

# Calculate average metrics for display
avg_profile = df['profile'].value_counts().idxmax()
avg_driving_pattern = df['driving_pattern'].value_counts().idxmax()
avg_severity_factor = df['severity_factor'].mean()
avg_cluster_risk = df['cluster_risk'].mean()
avg_research_data = df['research_data'].mean()
avg_weighted_risk = df['weighted_risk'].mean()

# Layout
app.layout = html.Div([
    html.H1('Iroute Management Dashboard', style={'textAlign': 'center', 'color': '#0074D9'}),
    
    # Key Metrics
    html.Div([
        html.Div([
            html.H3('0.8% Resilient Driver', style={'color': '#FF4136'}),
            html.H3('0.27% Insurance Driving', style={'color': '#FF851B'}),
            html.H3('25.1% Safe Driving', style={'color': '#2ECC40'}),
            html.H3('45% Computer Scoring', style={'color': '#0074D9'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
    ]),
    
    # Driving Scores
    html.Div([
        html.Div([
            dcc.Graph(
                figure=px.pie(
                    names=['Tactical Driving', 'Technical Driving'],
                    values=[60, 40],
                    title='Professional Driving Score',
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                figure=px.pie(
                    names=['Speed', 'Acceleration', 'Braking'],
                    values=[40, 30, 30],
                    title='Tactical Driving Score',
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'margin-bottom': '20px'}),
    
    # Interactive Event Log
    html.Div([
        dcc.Graph(
            figure=px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                color='event',
                hover_data={'latitude': False, 'longitude': False, 'timestamp': True, 'speed': True},
                zoom=10,
                height=400,
                mapbox_style="carto-positron"
            )
        )
    ], style={'margin-bottom': '20px'}),
    
    # Risk Assessment and Prediction
    html.Div([
        html.H3('Risk Assessment and Prediction', style={'color': '#0074D9'}),
        html.Div([
            html.P(f'Driver Profile Determination: {avg_profile}', style={'color': '#FF4136'}),
            html.P(f'Driving Patterns Identification: {avg_driving_pattern}', style={'color': '#FF851B'}),
            html.P(f'Severity Factor Calculation: {avg_severity_factor:.2f}', style={'color': '#2ECC40'}),
            html.P(f'Cluster Risk Calculation: {avg_cluster_risk:.2f}', style={'color': '#0074D9'}),
            html.P(f'Research Data Aggregation: {avg_research_data:.2f}', style={'color': '#FF4136'}),
            html.P(f'Weighted Risk Factor: {avg_weighted_risk:.2f}', style={'color': '#FF851B'})
        ])
    ], style={'margin-bottom': '20px'}),
    
    # Strongest Correlations
    html.Div([
        html.H3('Strongest Correlations', style={'color': '#0074D9'}),
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': '#0074D9',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
        )
    ], style={'margin-bottom': '20px'}),
    
    # Daily Records
    html.Div([
        dcc.Graph(
            figure=px.bar(
                df,
                x='timestamp',
                y='speed',
                title='Daily Records',
                color='speed',
                color_continuous_scale=px.colors.sequential.Plasma
            )
        )
    ], style={'margin-bottom': '20px'}),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)