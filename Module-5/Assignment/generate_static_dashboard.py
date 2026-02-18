"""
Generate static HTML dashboard for PDF export
Module 5 Assignment - AAI-530
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

# Color scheme
COLORS = {
    'actual': '#3498DB',      # Blue
    'predicted': '#F39C12',   # Orange
    'alert': '#E74C3C',       # Red
    'success': '#2ECC71',     # Green
}

CATEGORY_COLORS = {
    'Low Usage': '#2ECC71',
    'Normal Usage': '#3498DB',
    'High Usage': '#F39C12',
    'Very High Usage': '#E74C3C'
}

# Load data
print("Loading data...")
df = pd.read_csv('household_power_tableau.csv')
df['Datetime'] = pd.to_datetime(df['Datetime'])
daily_stats = pd.read_csv('daily_summary_tableau.csv')
daily_stats['Date'] = pd.to_datetime(daily_stats['Date'])

print(f"Data loaded: {len(df)} rows")

# Create subplots layout
fig = make_subplots(
    rows=4, cols=3,
    row_heights=[0.25, 0.25, 0.25, 0.25],
    column_widths=[0.4, 0.3, 0.3],
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}, {"type": "pie"}],
        [{"type": "bar", "colspan": 3}, None, None],
        [{"type": "scatter", "colspan": 2}, None, {"type": "histogram"}],
        [{"type": "table", "colspan": 3}, None, None]
    ],
    subplot_titles=(
        "Current Power Consumption (kW)",
        "High Power Alerts",
        "Circuit Breakdown",
        "Average Daily Power Consumption",
        "Power Consumption: Actual vs ML Prediction (Last 3 Days)",
        "",
        "ML Prediction Error Distribution",
        "Summary Statistics"
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.08
)

# 1. Current Power Status (Indicator)
current_power = df['Global_active_power'].iloc[-1]
current_category = df['Usage_Category'].iloc[-1]
current_color = CATEGORY_COLORS[current_category]

fig.add_trace(go.Indicator(
    mode="number",
    value=current_power,
    number={'suffix': " kW", 'font': {'size': 60, 'color': current_color}},
    title={'text': f"<b>{current_category}</b>", 'font': {'size': 16}},
), row=1, col=1)

# 2. Alert Count (Indicator)
alert_count = df['High_Power_Alert'].sum()
fig.add_trace(go.Indicator(
    mode="number",
    value=alert_count,
    number={'font': {'size': 50, 'color': COLORS['alert']}},
    title={'text': "<b>&gt;5 kW<br>Last 14 Days</b>", 'font': {'size': 12}},
), row=1, col=2)

# 3. Circuit Breakdown (Pie Chart)
kitchen_avg = df['Sub_metering_1'].mean()
laundry_avg = df['Sub_metering_2'].mean()
climate_avg = df['Sub_metering_3'].mean()

fig.add_trace(go.Pie(
    labels=['Kitchen', 'Laundry', 'Climate'],
    values=[kitchen_avg, laundry_avg, climate_avg],
    marker=dict(colors=['#E67E22', '#9B59B6', '#16A085']),
    textposition='inside',
    textinfo='percent+label'
), row=1, col=3)

# 4. Daily Trends (Bar Chart)
daily_avg = df.groupby(df['Datetime'].dt.date).agg({
    'Global_active_power': 'mean',
    'Usage_Category': lambda x: x.mode()[0] if len(x) > 0 else 'Normal Usage'
}).reset_index()
daily_avg.columns = ['Date', 'Avg_Power', 'Category']

for category in ['Low Usage', 'Normal Usage', 'High Usage', 'Very High Usage']:
    category_data = daily_avg[daily_avg['Category'] == category]
    if len(category_data) > 0:
        fig.add_trace(go.Bar(
            x=category_data['Date'],
            y=category_data['Avg_Power'],
            name=category,
            marker_color=CATEGORY_COLORS[category],
            showlegend=True
        ), row=2, col=1)

# Add average reference line
overall_avg = daily_avg['Avg_Power'].mean()
all_dates = daily_avg['Date'].tolist()
fig.add_trace(go.Scatter(
    x=all_dates,
    y=[overall_avg] * len(all_dates),
    mode='lines',
    name=f'14-Day Avg: {overall_avg:.2f} kW',
    line=dict(color='#95A5A6', width=2, dash='dash'),
    showlegend=True
), row=2, col=1)

# 5. Prediction vs Actual (Line Chart - Last 3 days)
last_3_days = df['Datetime'].max() - pd.Timedelta(days=3)
df_recent = df[df['Datetime'] >= last_3_days]

fig.add_trace(go.Scatter(
    x=df_recent['Datetime'],
    y=df_recent['Global_active_power'],
    mode='lines',
    name='Actual',
    line=dict(color=COLORS['actual'], width=2),
    showlegend=True
), row=3, col=1)

fig.add_trace(go.Scatter(
    x=df_recent['Datetime'],
    y=df_recent['Predicted_Power'],
    mode='lines',
    name='Predicted',
    line=dict(color=COLORS['predicted'], width=2, dash='dash'),
    showlegend=True
), row=3, col=1)

# 6. Prediction Error Distribution (Histogram)
fig.add_trace(go.Histogram(
    x=df['Prediction_Error'],
    nbinsx=25,
    marker=dict(
        color=COLORS['predicted'],
        line=dict(color='white', width=1)
    ),
    showlegend=False,
    name='Error Distribution'
), row=3, col=3)

mean_error = df['Prediction_Error'].mean()

# 7. Summary Statistics Table
stats_data = {
    'Metric': [
        'Average Power',
        'Max Power',
        'Min Power',
        'High Power Alerts',
        'Avg Prediction Error',
        'Data Points',
        'Date Range'
    ],
    'Value': [
        f"{df['Global_active_power'].mean():.2f} kW",
        f"{df['Global_active_power'].max():.2f} kW",
        f"{df['Global_active_power'].min():.2f} kW",
        f"{df['High_Power_Alert'].sum()}",
        f"{df['Prediction_Error'].mean():.3f} kW",
        f"{len(df):,}",
        f"{df['Datetime'].min().strftime('%Y-%m-%d')} to {df['Datetime'].max().strftime('%Y-%m-%d')}"
    ]
}

fig.add_trace(go.Table(
    header=dict(
        values=['<b>Metric</b>', '<b>Value</b>'],
        fill_color='#3498DB',
        font=dict(color='white', size=14),
        align='left'
    ),
    cells=dict(
        values=[stats_data['Metric'], stats_data['Value']],
        fill_color='#ECF0F1',
        font=dict(size=12),
        align='left',
        height=25
    )
), row=4, col=1)

# Update layout
fig.update_layout(
    title={
        'text': '<b>⚡ Smart Home Energy Monitoring Dashboard</b><br><sub>IoT System with ML-Powered Predictions | AAI-530 Module 5</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24}
    },
    height=2000,
    showlegend=True,
    barmode='stack',
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.48,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=11)
)

# Update axes
fig.update_xaxes(title_text="Date", row=2, col=1, showgrid=True, gridcolor='#E5E5E5')
fig.update_yaxes(title_text="Power (kW)", row=2, col=1, showgrid=True, gridcolor='#E5E5E5')

fig.update_xaxes(title_text="Time", row=3, col=1, showgrid=True, gridcolor='#E5E5E5')
fig.update_yaxes(title_text="Power (kW)", row=3, col=1, showgrid=True, gridcolor='#E5E5E5')

fig.update_xaxes(title_text="Prediction Error (kW)", row=3, col=3, showgrid=True, gridcolor='#E5E5E5')
fig.update_yaxes(title_text="Frequency", row=3, col=3, showgrid=True, gridcolor='#E5E5E5')

# Save as HTML (with embedded plotly)
print("Generating HTML file...")
html_file = 'Energy_Monitoring_Dashboard.html'
fig.write_html(
    html_file,
    config={'displayModeBar': True, 'displaylogo': False},
    include_plotlyjs='cdn'
)
print(f"Dashboard saved as {html_file}")

# Save as static image (PNG)
print("Generating PNG image...")
try:
    fig.write_image('Energy_Monitoring_Dashboard.png', width=1400, height=2000, scale=2)
    print("Dashboard saved as Energy_Monitoring_Dashboard.png")
except Exception as e:
    print(f"Could not save as PNG: {e}")

# Save as PDF directly using kaleido
print("Generating PDF...")
try:
    fig.write_image('Energy_Monitoring_Dashboard.pdf', width=1400, height=2000, format='pdf')
    print("Dashboard saved as Energy_Monitoring_Dashboard.pdf")
    print("\n✓ PDF ready for submission!")
except Exception as e:
    print(f"Could not save as PDF: {e}")
    print("\nTo convert to PDF manually:")
    print(f"1. Open {html_file} in a web browser")
    print("2. Press Ctrl+P (or Cmd+P on Mac)")
    print("3. Select 'Save as PDF'")
    print("4. Set paper size to A3 or Tabloid (Landscape)")
    print("5. Save as 'Energy_Monitoring_Dashboard.pdf'")
