# Assignment 5.1: Tableau Dashboard Creation Guide
## Household Energy Consumption IoT Monitoring Dashboard

### Dataset Overview
You now have two CSV files ready for Tableau:
- **household_power_tableau.csv**: 4,032 data points (2 weeks, 5-min intervals)
- **daily_summary_tableau.csv**: 15 days of aggregated statistics

This represents an IoT smart home energy monitoring system with ML predictions for power consumption.

---

## Part 1: Setup Tableau Public

### Step 1: Install Tableau Public
1. Go to https://public.tableau.com/
2. Click "Sign Up" (create free account with your email)
3. Download "Tableau Public" desktop application
4. Install and launch the application

### Step 2: Connect to Data
1. Open Tableau Public Desktop
2. Under "Connect" → "To a File" → select "Text file"
3. Navigate to `/home/margonza/Documents/Marco/Master/AAI-530-IN1/AAI-530-USD/Module-5/Assignment/`
4. Select **household_power_tableau.csv**
5. Click the data source tab at bottom to verify data loaded correctly
6. Check that "Datetime" is recognized as Date & Time (not String)
   - If not: Click the data type icon and change to "Date & Time"

---

## Part 2: Create Visualizations

### Visualization 1: CURRENT POWER STATUS (Summary/Status)
**Purpose**: Show current power consumption at a glance

**Steps**:
1. Create new worksheet (Sheet 1), rename to "Current Status"
2. Drag **Global_active_power** to Text on Marks card
3. Right-click on SUM(Global_active_power) → Measure → Maximum
   - This shows the most recent value (streaming simulation)
4. Click on "Text" in Marks card → Format:
   - Font size: 72pt
   - Bold
   - Alignment: Center
5. Drag **Usage_Category** to Color on Marks card
6. Edit colors:
   - Low Usage: Green (#2ECC71)
   - Normal Usage: Blue (#3498DB)
   - High Usage: Orange (#F39C12)
   - Very High Usage: Red (#E74C3C)
7. Add title: "Current Power Consumption (kW)"
8. Remove axes and gridlines for clean display

### Visualization 2: DAILY USAGE SUMMARY (Summary)
**Purpose**: Show power usage trends over the past 2 weeks

**Steps**:
1. Create new worksheet, rename to "Daily Trends"
2. Drag **Datetime** to Columns
   - Right-click → click "Day" (not hour/minute)
3. Drag **Global_active_power** to Rows
4. Right-click SUM(Global_active_power) → Measure → Average
5. Change mark type to "Bar"
6. Drag **Usage_Category** to Color
7. Use same color scheme as Visualization 1
8. Add reference line:
   - Right-click Y-axis → Add Reference Line
   - Value: Average
   - Label: "14-Day Average"
9. Title: "Average Daily Power Consumption"
10. Format axes with 1 decimal place

### Visualization 3: ALERT COUNT STATUS (Summary/Status)
**Purpose**: Show number of high-power alerts

**Steps**:
1. Create new worksheet, rename to "Alert Status"
2. Create a calculated field:
   - Right-click in Data pane → Create Calculated Field
   - Name: "Total Alerts"
   - Formula: `SUM([High_Power_Alert])`
3. Drag "Total Alerts" to Text
4. Format as large number (size: 60pt, bold, red color)
5. Add "🔔" emoji or "⚠" symbol before number
6. Title: "High Power Alerts (>5 kW)"
7. Add subtitle: "Last 14 Days"

### Visualization 4: PREDICTION vs ACTUAL (Machine Learning)
**Purpose**: Show ML prediction accuracy over time

**Steps**:
1. Create new worksheet, rename to "ML Predictions"
2. Drag **Datetime** to Columns
3. Drag **Global_active_power** AND **Predicted_Power** to Rows
4. Right-click Datetime → select "Hour" to show hourly detail
5. For the dual axis:
   - Right-click second axis (Predicted_Power) → Dual Axis
   - Right-click second axis → Synchronize Axis
6. Format lines:
   - Global_active_power: Solid line, dark blue, size 2
   - Predicted_Power: Dashed line, orange, size 2
7. Add legend showing "Actual vs Predicted"
8. Title: "Power Consumption: Actual vs ML Prediction"
9. Filter to show last 3 days for clarity:
   - Drag Datetime to Filters
   - Select "Relative dates" → "Last 3 days"

### Visualization 5: PREDICTION ERROR DISTRIBUTION (ML Performance)
**Purpose**: Show accuracy of ML model

**Steps**:
1. Create new worksheet, rename to "Prediction Accuracy"
2. Drag **Prediction_Error** to Columns
3. Click "Show Me" → select Histogram
4. Adjust bin size to 0.1 kW
5. Color gradient from green (low error) to red (high error)
6. Add reference line at mean error
7. Title: "ML Prediction Error Distribution"
8. Subtitle: "Lower is better"

### Visualization 6: SUB-METERING BREAKDOWN (Summary)
**Purpose**: Show which circuits use most power

**Steps**:
1. Create new worksheet, rename to "Circuit Breakdown"
2. Create calculated fields for each:
   - "Kitchen": `AVG([Sub_metering_1])`
   - "Laundry": `AVG([Sub_metering_2])`
   - "Climate": `AVG([Sub_metering_3])`
3. Create a pie chart or horizontal bar chart
4. Use different colors for each circuit
5. Show percentage of total
6. Title: "Power Distribution by Circuit"

---

## Part 3: Create Dashboard

### Dashboard Layout
1. Click "Dashboard" → "New Dashboard" at bottom
2. Set size: "Automatic" or "Desktop (1000 x 800)"

### Arrange Visualizations
**Top Row** (Status at a glance):
- **Left**: Current Status (large, 40% width)
- **Right Top**: Alert Status (20% width)
- **Right Bottom**: Circuit Breakdown (20% width)

**Middle Row** (Trend analysis):
- **Full Width**: Daily Trends bar chart

**Bottom Row** (ML Performance):
- **Left** (60%): ML Predictions line chart
- **Right** (40%): Prediction Accuracy histogram

### Dashboard Formatting

**Color Scheme** (Consistent across all charts):
- Primary: Blue (#3498DB) for actual values
- Secondary: Orange (#F39C12) for predictions
- Alert: Red (#E74C3C) for warnings
- Success: Green (#2ECC71) for normal operation
- Background: Light gray (#ECF0F1) or white

**Typography**:
- Dashboard Title: 24pt, Bold, Dark gray
- Viz Titles: 14pt, Bold
- Labels: 11pt, Regular
- Data values: 12pt, Bold where important

**Interactive Elements**:
1. Add filters as dropdown:
   - Date range selector
   - Usage category filter
2. Enable "Highlight" actions:
   - Dashboard → Actions → Add Action → Highlight
   - When you click a bar in Daily Trends, it highlights in other charts

**Final Polish**:
1. Add Dashboard Title: "Smart Home Energy Monitoring Dashboard"
2. Add subtitle: "IoT System with ML-Powered Predictions"
3. Add text box with current status:
   - "🟢 System Online | Last Update: [Datetime]"
4. Ensure no overlapping elements
5. Test all interactions work

---

## Part 4: Publish and Export

### Publish to Tableau Public
1. File → Save to Tableau Public
2. Sign in with your account
3. Give it a name: "IoT-Energy-Monitoring-Dashboard"
4. Click "Save"
5. **Copy the public URL** (you'll need this for submission)

### Export as PDF
1. Dashboard → Export as PDF
2. Save to: `/home/margonza/Documents/Marco/Master/AAI-530-IN1/AAI-530-USD/Module-5/Assignment/`
3. Filename: `Energy_Monitoring_Dashboard.pdf`
4. Make sure all visualizations are visible

---

## Design Tips

### Pre-attentive Attributes Used:
1. **Color**: Red for alerts, green for normal, blue for data
2. **Size**: Larger fonts for critical metrics (current power, alerts)
3. **Position**: Most important info at top
4. **Intensity**: Gradient colors for error magnitude

### Streaming Dashboard Considerations:
- Use "latest value" aggregations (MAX of timestamp)
- Keep time windows recent (last 3 days, last 14 days)
- Show current status prominently
- Include alert counts for anomalies
- Real-time updates would use Tableau's refresh feature

### User-Friendly Design:
- Clear labels on all charts
- Legends positioned consistently
- Minimal clutter
- Logical flow: Status → Trends → Predictions
- Accessible colors (colorblind-safe palette)

---

## Submission Checklist

✅ Dashboard has 2+ summary/status visualizations
✅ Dashboard has 1+ machine learning visualization
✅ All visualizations use consistent color scheme
✅ Layout is clean and user-friendly
✅ Pre-attentive attributes highlight important info
✅ Charts interact with each other
✅ Published to Tableau Public (got URL)
✅ Exported as PDF
✅ Submit PDF + Tableau Public URL on Canvas

---

## Troubleshooting

**Issue**: Datetime showing as string
- **Fix**: Click data type icon in data source tab → change to Date & Time

**Issue**: Charts look crowded
- **Fix**: Use filters to show recent data only (last 3-7 days)

**Issue**: Can't publish to Tableau Public
- **Fix**: Make sure you saved your Tableau Public credentials, check internet connection

**Issue**: PDF export cuts off visualizations
- **Fix**: Adjust dashboard size before exporting, or export as image instead

---

Good luck! The dashboard simulates a real-time IoT energy monitoring system with ML predictions, perfect for demonstrating data visualization skills in an IoT context.
