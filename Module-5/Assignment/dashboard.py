"""
Smart Home Energy Monitoring Dashboard
IoT System with ML-Powered Predictions
Module 5 Assignment - AAI-530
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Smart Home Energy Monitoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme (matching Tableau guide)
COLORS = {
    'actual': '#3498DB',      # Blue
    'predicted': '#F39C12',   # Orange
    'alert': '#E74C3C',       # Red
    'success': '#2ECC71',     # Green
    'low': '#2ECC71',         # Low Usage - Green
    'normal': '#3498DB',      # Normal Usage - Blue
    'high': '#F39C12',        # High Usage - Orange
    'very_high': '#E74C3C',   # Very High Usage - Red
}

CATEGORY_COLORS = {
    'Low Usage': COLORS['low'],
    'Normal Usage': COLORS['normal'],
    'High Usage': COLORS['high'],
    'Very High Usage': COLORS['very_high']
}

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('household_power_tableau.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    daily = pd.read_csv('daily_summary_tableau.csv')
    daily['Date'] = pd.to_datetime(daily['Date'])
    return df, daily

df, daily_stats = load_data()

# Dashboard Title
st.markdown("""
    <h1 style='text-align: center; color: #2C3E50; margin-bottom: 0;'>
        ⚡ Smart Home Energy Monitoring Dashboard
    </h1>
    <p style='text-align: center; color: #7F8C8D; font-size: 16px; margin-top: 5px;'>
        IoT System with ML-Powered Predictions
    </p>
    """, unsafe_allow_html=True)

# Status bar
current_time = df['Datetime'].max()
total_alerts = df['High_Power_Alert'].sum()
status_color = COLORS['success'] if total_alerts < 5 else COLORS['alert']

st.markdown(f"""
    <div style='background-color: #ECF0F1; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>
        <span style='color: {status_color}; font-size: 14px;'>● System Online</span>
        <span style='color: #7F8C8D; margin-left: 20px;'>Last Update: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")

# Date range filter
min_date = df['Datetime'].min().date()
max_date = df['Datetime'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Usage category filter
categories = st.sidebar.multiselect(
    "Usage Categories",
    options=['Low Usage', 'Normal Usage', 'High Usage', 'Very High Usage'],
    default=['Low Usage', 'Normal Usage', 'High Usage', 'Very High Usage']
)

# Apply filters
if len(date_range) == 2:
    mask = (df['Datetime'].dt.date >= date_range[0]) & (df['Datetime'].dt.date <= date_range[1])
    df_filtered = df[mask]
else:
    df_filtered = df

if categories:
    df_filtered = df_filtered[df_filtered['Usage_Category'].isin(categories)]

# ========== TOP ROW: STATUS AT A GLANCE ==========
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("### 🔌 Current Power Consumption")
    # Get current (latest) power reading
    current_power = df_filtered['Global_active_power'].iloc[-1]
    current_category = df_filtered['Usage_Category'].iloc[-1]
    current_color = CATEGORY_COLORS[current_category]

    st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #F8F9FA; border-radius: 10px;'>
            <h1 style='color: {current_color}; font-size: 72px; margin: 0;'>{current_power:.2f}</h1>
            <p style='color: #7F8C8D; font-size: 20px; margin-top: 10px;'>kW</p>
            <p style='color: {current_color}; font-size: 16px; font-weight: bold;'>{current_category}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🔔 High Power Alerts")
    alert_count = df_filtered['High_Power_Alert'].sum()
    st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #F8F9FA; border-radius: 10px;'>
            <h1 style='color: {COLORS['alert']}; font-size: 60px; margin: 0;'>⚠ {alert_count}</h1>
            <p style='color: #7F8C8D; font-size: 14px; margin-top: 10px;'>Alerts (&gt;5 kW)</p>
            <p style='color: #7F8C8D; font-size: 12px;'>Last 14 Days</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("### 🏠 Circuit Breakdown")
    # Calculate average sub-metering
    kitchen_avg = df_filtered['Sub_metering_1'].mean()
    laundry_avg = df_filtered['Sub_metering_2'].mean()
    climate_avg = df_filtered['Sub_metering_3'].mean()

    circuit_data = pd.DataFrame({
        'Circuit': ['Kitchen', 'Laundry', 'Climate'],
        'Power': [kitchen_avg, laundry_avg, climate_avg]
    })

    fig_pie = px.pie(
        circuit_data,
        values='Power',
        names='Circuit',
        color='Circuit',
        color_discrete_map={'Kitchen': '#E67E22', 'Laundry': '#9B59B6', 'Climate': '#16A085'}
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        showlegend=False,
        height=250,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ========== MIDDLE ROW: TREND ANALYSIS ==========
st.markdown("### 📈 Average Daily Power Consumption")

# Aggregate by day
daily_avg = df_filtered.groupby(df_filtered['Datetime'].dt.date).agg({
    'Global_active_power': 'mean',
    'Usage_Category': lambda x: x.mode()[0] if len(x) > 0 else 'Normal Usage'
}).reset_index()
daily_avg.columns = ['Date', 'Avg_Power', 'Category']

# Create bar chart
fig_daily = go.Figure()
for category in ['Low Usage', 'Normal Usage', 'High Usage', 'Very High Usage']:
    category_data = daily_avg[daily_avg['Category'] == category]
    fig_daily.add_trace(go.Bar(
        x=category_data['Date'],
        y=category_data['Avg_Power'],
        name=category,
        marker_color=CATEGORY_COLORS[category]
    ))

# Add reference line for average
overall_avg = daily_avg['Avg_Power'].mean()
fig_daily.add_hline(
    y=overall_avg,
    line_dash="dash",
    line_color="#95A5A6",
    annotation_text=f"14-Day Average: {overall_avg:.2f} kW",
    annotation_position="top left"
)

fig_daily.update_layout(
    barmode='stack',
    xaxis_title="Date",
    yaxis_title="Average Power (kW)",
    height=400,
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_daily, use_container_width=True)

# ========== BOTTOM ROW: ML PERFORMANCE ==========
col4, col5 = st.columns([3, 2])

with col4:
    st.markdown("### 🤖 Power Consumption: Actual vs ML Prediction")

    # Show last 3 days for clarity
    last_3_days = df_filtered['Datetime'].max() - pd.Timedelta(days=3)
    df_recent = df_filtered[df_filtered['Datetime'] >= last_3_days]

    fig_pred = go.Figure()

    # Actual values
    fig_pred.add_trace(go.Scatter(
        x=df_recent['Datetime'],
        y=df_recent['Global_active_power'],
        mode='lines',
        name='Actual',
        line=dict(color=COLORS['actual'], width=2),
        hovertemplate='<b>Actual</b><br>Time: %{x}<br>Power: %{y:.3f} kW<extra></extra>'
    ))

    # Predicted values
    fig_pred.add_trace(go.Scatter(
        x=df_recent['Datetime'],
        y=df_recent['Predicted_Power'],
        mode='lines',
        name='Predicted',
        line=dict(color=COLORS['predicted'], width=2, dash='dash'),
        hovertemplate='<b>Predicted</b><br>Time: %{x}<br>Power: %{y:.3f} kW<extra></extra>'
    ))

    fig_pred.update_layout(
        xaxis_title="Time",
        yaxis_title="Power (kW)",
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_pred, use_container_width=True)

with col5:
    st.markdown("### 📊 ML Prediction Error Distribution")

    # Create histogram
    fig_error = go.Figure()
    fig_error.add_trace(go.Histogram(
        x=df_filtered['Prediction_Error'],
        nbinsx=30,
        marker=dict(
            color=df_filtered['Prediction_Error'],
            colorscale=[[0, COLORS['success']], [1, COLORS['alert']]],
            showscale=False
        ),
        hovertemplate='Error Range: %{x:.2f} kW<br>Count: %{y}<extra></extra>'
    ))

    # Add mean error line
    mean_error = df_filtered['Prediction_Error'].mean()
    fig_error.add_vline(
        x=mean_error,
        line_dash="dash",
        line_color="#34495E",
        annotation_text=f"Mean: {mean_error:.3f} kW",
        annotation_position="top"
    )

    fig_error.update_layout(
        xaxis_title="Prediction Error (kW)",
        yaxis_title="Frequency",
        height=400,
        showlegend=False
    )

    st.plotly_chart(fig_error, use_container_width=True)

    st.markdown(f"""
        <p style='text-align: center; color: #7F8C8D; font-size: 12px; font-style: italic;'>
            Lower is better • Avg Error: {mean_error:.3f} kW
        </p>
        """, unsafe_allow_html=True)

# ========== STATISTICS SUMMARY ==========
st.markdown("---")
st.markdown("### 📋 Summary Statistics")

stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)

with stat_col1:
    st.metric("Average Power", f"{df_filtered['Global_active_power'].mean():.2f} kW")

with stat_col2:
    st.metric("Max Power", f"{df_filtered['Global_active_power'].max():.2f} kW")

with stat_col3:
    st.metric("High Power Alerts", f"{df_filtered['High_Power_Alert'].sum()}")

with stat_col4:
    st.metric("Avg Prediction Error", f"{df_filtered['Prediction_Error'].mean():.3f} kW")

with stat_col5:
    st.metric("Data Points", f"{len(df_filtered):,}")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #95A5A6; font-size: 12px; padding: 20px;'>
        <p>🤖 Smart Home Energy Monitoring Dashboard | IoT System with ML-Powered Predictions</p>
        <p>AAI-530 Module 5 Assignment | Data Visualization with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
