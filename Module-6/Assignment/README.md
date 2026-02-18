# Assignment 6.1: Pre-Trained Generative Model for IoT
## Daily RAN Network Health Report Generator

### Overview

This assignment demonstrates the integration of a pre-trained generative AI model (OpenAI GPT-4) with an IoT application for automated network health reporting in 5G Radio Access Networks.

### Use Case

**Problem**: Network operations teams monitor thousands of 5G base stations generating massive volumes of telemetry data. Identifying critical issues and trends from raw metrics is time-consuming and requires expert knowledge.

**Solution**: An automated system that uses generative AI to transform daily RAN telemetry data into clear, actionable health reports with:
- Executive summaries for leadership
- Critical issue identification
- Capacity trend analysis
- Specific operational recommendations

### Files

- `Generative_AI_IoT_Assignment.ipynb` - Main Jupyter notebook with code and documentation
- `Generative_AI_IoT_Assignment.pdf` - PDF export for Canvas submission
- `README.md` - This file

### Components

✅ **IoT Use Case Description**: Daily RAN network health reporting for telecom operators

✅ **API Connection**: OpenAI GPT-4 via official Python SDK

✅ **Input Structure**: JSON telemetry data from RAN IoT sensors including:
- Performance metrics (throughput, latency, packet loss)
- Resource utilization (CPU, memory, bandwidth)
- Quality indicators (handover success, call drops)
- Alerts and top issues
- Capacity trends

✅ **Prompt Engineering**: Structured prompts that instruct the AI model to:
- Act as a network operations analyst
- Apply domain-specific performance thresholds
- Generate reports with specific sections
- Provide actionable recommendations

✅ **Model Output**: Natural language daily health report with:
- Executive summary
- Key performance metrics
- Critical issues requiring attention
- Capacity analysis and trends
- Prioritized recommendations (immediate, short-term, strategic)

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install openai jupyter
   ```

2. **Set API Key** (required for actual execution):
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

   Get a free API key at: https://platform.openai.com/api-keys

3. **Run Notebook**:
   ```bash
   jupyter notebook Generative_AI_IoT_Assignment.ipynb
   ```

### Example Output

The notebook includes a detailed example of the generated report showing how the AI transforms:

**Input (JSON telemetry data):**
```json
{
  "avg_throughput_mbps": 485.3,
  "avg_cpu_utilization_pct": 67.2,
  "critical_alerts": 3,
  "top_issues": [
    {"cell_id": "CELL-089", "issue": "High CPU", "value": "94.2%"}
  ]
}
```

**Output (Natural language report):**
```
## Critical Issues

🔴 CELL-089: Sustained High CPU Utilization
   - Issue: CPU at 94.2% for 8.3 hours
   - Impact: Risk of service degradation
   - Action: Immediate investigation; load balancing required
```

### Real-World Applicability

This pattern is used in production IoT systems for:
- **Telecommunications**: Daily network health reports (as demonstrated)
- **Industrial IoT**: Equipment health summaries from sensor data
- **Smart Buildings**: Energy consumption reports for facility managers
- **Healthcare**: Patient monitoring summaries from wearable devices
- **Agriculture**: Crop health reports from soil and weather sensors

### Assignment Requirements Met

✅ Quick description of model use (Daily RAN health reporting)
✅ Connection to generative AI API (OpenAI GPT-4)
✅ Code instructing model interaction (Structured prompts with JSON input)
✅ Model output relevant to IoT use case (Example network health report)
✅ Well-defined IoT application (5G RAN telemetry monitoring)
✅ Successful API integration (Using official OpenAI Python SDK)

### Technologies Used

- **Python 3.11**: Programming language
- **OpenAI GPT-4**: Large language model for text generation
- **JSON**: Data interchange format for telemetry
- **Jupyter Notebook**: Interactive development environment

### Author

Marco Gonzalez
AAI-530 - Introduction to IoT
University of San Diego
February 2026
