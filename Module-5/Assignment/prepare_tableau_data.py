"""
Prepare Household Energy Consumption dataset with ML predictions for Tableau visualization
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Load the cleaned household power consumption data
print("Loading data...")
df = pd.read_csv('/home/margonza/Documents/Marco/Master/AAI-530-IN1/AAI-530-USD/Module-3/Assignment/household_power_clean.csv')

# Convert datetime
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Take a manageable subset: 2 weeks of recent data (every 5 minutes for smaller file)
# This gives us ~4000 data points instead of 2 million
df = df.sort_values('Datetime')
df_subset = df.iloc[-20160::5].copy()  # Last 2 weeks, every 5 minutes

print(f"Dataset size: {len(df_subset)} rows")
print(f"Date range: {df_subset['Datetime'].min()} to {df_subset['Datetime'].max()}")

# Create time-based features for ML
df_subset['Hour'] = df_subset['Datetime'].dt.hour
df_subset['DayOfWeek'] = df_subset['Datetime'].dt.dayofweek
df_subset['IsWeekend'] = (df_subset['DayOfWeek'] >= 5).astype(int)

# Create ML predictions using simple linear regression
# Predict Global_active_power based on recent history
print("Creating ML predictions...")

predictions = []
for i in range(len(df_subset)):
    if i < 12:  # Need at least 12 points (1 hour of history)
        predictions.append(df_subset['Global_active_power'].iloc[i])
    else:
        # Use last 12 points to predict current value
        X = np.arange(12).reshape(-1, 1)
        y = df_subset['Global_active_power'].iloc[i-12:i].values

        # Simple linear regression
        model = LinearRegression()
        model.fit(X, y)
        pred = model.predict([[12]])[0]  # Predict next point
        predictions.append(pred)

df_subset['Predicted_Power'] = predictions

# Calculate prediction error
df_subset['Prediction_Error'] = abs(df_subset['Global_active_power'] - df_subset['Predicted_Power'])

# Create status categories for summary visualizations
def power_category(power):
    if power < 1.0:
        return 'Low Usage'
    elif power < 3.0:
        return 'Normal Usage'
    elif power < 5.0:
        return 'High Usage'
    else:
        return 'Very High Usage'

df_subset['Usage_Category'] = df_subset['Global_active_power'].apply(power_category)

# Create alert flags
df_subset['High_Power_Alert'] = (df_subset['Global_active_power'] > 5.0).astype(int)
df_subset['Poor_Prediction'] = (df_subset['Prediction_Error'] > 1.0).astype(int)

# Calculate daily statistics for summary views
df_subset['Date'] = df_subset['Datetime'].dt.date
daily_stats = df_subset.groupby('Date').agg({
    'Global_active_power': ['mean', 'max', 'min'],
    'Voltage': 'mean',
    'Global_intensity': 'mean',
    'High_Power_Alert': 'sum'
}).reset_index()

daily_stats.columns = ['Date', 'Avg_Power', 'Max_Power', 'Min_Power', 'Avg_Voltage', 'Avg_Intensity', 'Alert_Count']

# Prepare final dataset
output_columns = [
    'Datetime',
    'Global_active_power',
    'Predicted_Power',
    'Prediction_Error',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3',
    'Hour',
    'DayOfWeek',
    'IsWeekend',
    'Usage_Category',
    'High_Power_Alert',
    'Poor_Prediction'
]

df_final = df_subset[output_columns].copy()

# Save for Tableau
print("Saving datasets...")
df_final.to_csv('/home/margonza/Documents/Marco/Master/AAI-530-IN1/AAI-530-USD/Module-5/Assignment/household_power_tableau.csv', index=False)
daily_stats.to_csv('/home/margonza/Documents/Marco/Master/AAI-530-IN1/AAI-530-USD/Module-5/Assignment/daily_summary_tableau.csv', index=False)

print(f"\nDataset prepared successfully!")
print(f"Main dataset: {len(df_final)} rows")
print(f"Daily summary: {len(daily_stats)} rows")
print(f"\nFiles created:")
print("  - household_power_tableau.csv")
print("  - daily_summary_tableau.csv")

# Print summary statistics
print(f"\nData Summary:")
print(f"  Average Power: {df_final['Global_active_power'].mean():.2f} kW")
print(f"  Max Power: {df_final['Global_active_power'].max():.2f} kW")
print(f"  High Power Alerts: {df_final['High_Power_Alert'].sum()}")
print(f"  Average Prediction Error: {df_final['Prediction_Error'].mean():.3f} kW")
print(f"\nUsage Categories:")
print(df_final['Usage_Category'].value_counts())
