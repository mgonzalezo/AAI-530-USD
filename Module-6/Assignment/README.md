# Assignment 6.1: Pre-Trained Generative Model for IoT
## Daily NB-IoT Core Network Health Report Generator

### Overview

This assignment demonstrates the integration of a pre-trained generative AI model (OpenAI GPT-4) with an IoT application for automated network health reporting in Narrowband IoT (NB-IoT) Core networks.

### Use Case

**Problem**: Network operations teams monitor NB-IoT Core networks supporting millions of low-power IoT devices (smart meters, sensors, trackers). Core network elements generate massive volumes of telemetry data covering device attach procedures, session management, and power optimization. Identifying critical issues affecting IoT device connectivity from raw metrics is time-consuming and requires expert knowledge.

**Solution**: An automated system that uses generative AI to transform daily NB-IoT Core telemetry data into clear, actionable health reports with:
- Executive summaries for leadership
- Critical issue identification for IoT device connectivity
- Device growth and capacity trend analysis
- Power optimization monitoring (PSM, eDRX)
- Specific operational recommendations

### Files

- `Generative_AI_IoT_Assignment.ipynb` - Main Jupyter notebook with code and documentation
- `Generative_AI_IoT_Assignment.pdf` - PDF export for Canvas submission
- `README.md` - This file

### Components

✅ **IoT Use Case Description**: Daily NB-IoT Core network health reporting for telecom operators managing millions of IoT devices

✅ **API Connection**: OpenAI GPT-4 via official Python SDK

✅ **Input Structure**: JSON telemetry data from NB-IoT Core network elements including:
- Device attach and PDN session metrics (success rates, failures)
- IoT device population statistics (2.8M+ devices)
- Power optimization features (PSM, eDRX adoption)
- MME, S-GW, P-GW, HSS performance metrics
- Authentication and session management statistics
- Coverage enhancement level distribution
- Alerts and top issues
- Device growth and capacity trends

✅ **Prompt Engineering**: Structured prompts that instruct the AI model to:
- Act as a Core network operations analyst specializing in NB-IoT
- Apply domain-specific performance thresholds for IoT connectivity
- Generate reports with specific sections focused on device health
- Provide actionable recommendations for IoT Core optimization

✅ **Model Output**: Natural language daily health report with:
- Executive summary of IoT device connectivity health
- Key performance metrics for Core network elements
- Critical issues affecting IoT devices
- Device growth trends and power optimization analysis
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
- **NB-IoT Core Networks**: Daily device connectivity health reports (as demonstrated)
- **Smart Utilities**: Smart meter aggregation and anomaly detection
- **Industrial IoT**: Equipment health summaries from sensor data
- **Smart Cities**: Asset tracking and infrastructure monitoring
- **Healthcare**: Patient monitoring summaries from wearable devices
- **Agriculture**: Crop health reports from soil and weather sensors

### Assignment Requirements Met

✅ Quick description of model use (Daily NB-IoT Core health reporting for millions of IoT devices)
✅ Connection to generative AI API (OpenAI GPT-4)
✅ Code instructing model interaction (Structured prompts with JSON input)
✅ Model output relevant to IoT use case (Example Core network health report)
✅ Well-defined IoT application (NB-IoT Core network telemetry monitoring)
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
