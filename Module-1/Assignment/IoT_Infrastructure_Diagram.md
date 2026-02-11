# IoT Infrastructure Diagram
## Cell Tower Remote Monitoring System (Wireless Telco Industry)

### Device: Cell Site Environmental & Equipment Monitor

```
┌──────────────────────────────────────────────────────────────────────┐
│              CELL TOWER REMOTE MONITORING SYSTEM                     │
│                                                                       │
│  ┌───────────────┐                          ┌──────────────────┐    │
│  │   DS18B20     │ (Equipment Cabinet)      │  MPU-6050        │    │
│  │  Temperature  │                          │  Vibration/      │    │
│  │    Sensor     │                          │  Accelerometer   │    │
│  │  ±0.5°C       │                          │  (Tower Base)    │    │
│  │  -55°C to     │                          │  ±2g-±16g range  │    │
│  │   125°C       │                          └────────┬─────────┘    │
│  └───────┬───────┘                                   │               │
│          │                                           │               │
│          │         ┌──────────────────┐              │               │
│          │         │                  │              │               │
│          └────────►│  STM32/nRF9160   │◄─────────────┘               │
│                    │ Microcontroller  │                              │
│  ┌──────────┐     │  with LTE-M/     │      ┌──────────────┐        │
│  │ DHT22    │     │  NB-IoT Modem    │      │  Magnetic    │        │
│  │ Humidity │────►│                  │◄─────│  Door Sensor │        │
│  │ Sensor   │     │ - LTE Cat-M1     │      │  (Reed Switch)│       │
│  │ (Shelter)│     │ - LTE Cat-NB1    │      │  (Door)      │        │
│  └──────────┘     │ - 64MHz ARM      │      └──────────────┘        │
│                   │   Cortex-M       │                               │
│  ┌──────────┐    └────────┬─────────┘      ┌──────────────┐        │
│  │ ACS712   │             │                 │   GPS Module │        │
│  │ Current  │─────────────┘                 │   NEO-6M     │        │
│  │ Sensor   │  GPIO/I2C/SPI/UART            │  (Location)  │        │
│  │ (Power)  │                               └──────────────┘        │
│  └──────────┘             │                                         │
│                           │                                          │
│                  ┌────────▼────────┐                                 │
│                  │  Power Supply   │                                 │
│                  │  12V DC Battery │                                 │
│                  │  + Solar Panel  │                                 │
│                  └─────────────────┘                                 │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          │ LTE-M / NB-IoT Connection
                          │ Cellular Bands: B1/B2/B3/B4/B5/B8/B12/B13/B20
                          │ Frequency: 700-2100 MHz
                          │
                   ┌──────▼───────┐
                   │  Cell Tower  │
                   │   (eNodeB)   │
                   │  LTE Network │
                   └──────┬───────┘
                          │
                          │ Operator Core Network
                          │ (EPC - Evolved Packet Core)
                          │
                   ┌──────▼────────┐
                   │   Packet Data │
                   │     Network   │
                   │   Gateway     │
                   │   (PGW/UPF)   │
                   └──────┬────────┘
                          │
                          │ Internet/Private APN
                          │
                   ┌──────▼─────────┐
                   │  CoAP Server / │
                   │  MQTT Broker   │
                   │  (AWS IoT/     │
                   │   Azure IoT)   │
                   └──────┬─────────┘
                          │
              ┌───────────┴────────────┐
              │                        │
      ┌───────▼────────┐       ┌──────▼─────────┐
      │  NOC Dashboard │       │  Cloud Storage │
      │  (Network Ops  │       │  + Analytics   │
      │   Center)      │       │  Platform      │
      └────────────────┘       └────────────────┘
```

## Network Architecture

### Connectivity Type
- **Primary**: LTE Cat-M1 (LTE-M) - Low Power Wide Area Network
- **Secondary**: LTE Cat-NB1 (NB-IoT) - Narrowband IoT
- **Fallback**: 2G GSM (being phased out)
- **Frequency Bands**: 700-2100 MHz (region dependent)
  - North America: B2, B4, B12, B13
  - Europe: B1, B3, B8, B20
  - Global: B1, B2, B3, B4, B5, B8, B12, B13, B20
- **Coverage**: Wide area (same as cellular network)
- **Data Rate**:
  - LTE-M: Up to 1 Mbps (uplink/downlink)
  - NB-IoT: ~250 kbps (downlink), ~20-250 kbps (uplink)

### Messaging Protocol
- **Primary Protocol**: CoAP (Constrained Application Protocol)
  - **Version**: CoAP RFC 7252
  - **Transport**: UDP (User Datagram Protocol)
  - **Port**: 5683 (non-secure) / 5684 (DTLS secure)
  - **Method**: RESTful (GET, POST, PUT, DELETE)
  - **Message Types**: CON, NON, ACK, RST

- **Alternative Protocol**: MQTT over TCP
  - **Version**: MQTT 3.1.1
  - **Transport**: TCP/IP
  - **Port**: 8883 (TLS/SSL encrypted)
  - **QoS Levels**: 0, 1, 2

- **Security**: DTLS 1.2 (for CoAP) / TLS 1.2+ (for MQTT)

### Data Transmission Topics/Endpoints

#### CoAP Endpoints
- `/tower/[tower-id]/temperature`
- `/tower/[tower-id]/humidity`
- `/tower/[tower-id]/power`
- `/tower/[tower-id]/vibration`
- `/tower/[tower-id]/door`
- `/tower/[tower-id]/gps`
- `/tower/[tower-id]/status`

#### MQTT Topics (if MQTT used)
- `telco/cell-tower/[tower-id]/sensors/temperature`
- `telco/cell-tower/[tower-id]/sensors/humidity`
- `telco/cell-tower/[tower-id]/sensors/power`
- `telco/cell-tower/[tower-id]/sensors/vibration`
- `telco/cell-tower/[tower-id]/sensors/door-status`
- `telco/cell-tower/[tower-id]/location/gps`
- `telco/cell-tower/[tower-id]/device/status`

## Data Flow

1. **Sensors → Microcontroller**: Analog/Digital signals via GPIO, I2C, SPI, UART
2. **Microcontroller → Cell Tower**: LTE-M/NB-IoT cellular connection
3. **Cell Tower → Core Network**: Through EPC (Evolved Packet Core)
4. **Core Network → Internet/Private APN**: Via Packet Gateway (PGW/UPF)
5. **Internet → CoAP Server/MQTT Broker**: Cloud-based IoT platform
6. **IoT Platform → End Users**:
   - Network Operations Center (NOC) dashboard
   - Cloud analytics and storage
   - Alert systems (SMS, email)
   - Maintenance scheduling systems

## Technical Specifications Summary

| Component | Type | Communication | Limitations |
|-----------|------|---------------|-------------|
| DS18B20 | Temperature | 1-Wire Digital | -55°C to +125°C range |
| DHT22 | Humidity/Temp | Digital (1-Wire) | 2 sec sampling rate |
| ACS712 | Current Sensor | Analog | ±5% accuracy |
| MPU-6050 | Accelerometer/Gyro | I2C | Vibration threshold config |
| Reed Switch | Magnetic Door | Digital GPIO | Binary on/off only |
| NEO-6M GPS | Location | UART | Cold start: 27s |
| nRF9160/STM32+Modem | MCU + Cellular | LTE-M/NB-IoT | 2G/3G/4G only (no 5G) |

## Wireless Telco Specific Features

### Network Characteristics
- **Power Saving Mode (PSM)**: Reduces power consumption during idle periods
- **Extended Discontinuous Reception (eDRX)**: Allows device to sleep longer between paging occasions
- **Coverage Enhancement**: Up to 20 dB gain compared to regular LTE
- **Mobility**: Supports handover between cells (LTE-M only)
- **Voice Support**: LTE-M supports VoLTE; NB-IoT is data-only
- **Latency**:
  - LTE-M: ~10-100ms
  - NB-IoT: ~1.6-10 seconds

### Operator Integration
- **SIM Authentication**: Uses standard UICC/eSIM for network authentication
- **APN Configuration**: Can use private APN for enterprise security
- **Quality of Service (QoS)**: Operator-defined QoS profiles
- **Roaming**: International roaming capability (operator dependent)
- **IMEI Tracking**: Device identification and whitelisting

## Environmental Considerations

- **Operating Temperature**: -40°C to 85°C (industrial grade)
- **Operating Humidity**: 0-95% RH (non-condensing)
- **Power Source**: 12V DC battery with solar charging
- **Power Consumption**:
  - Active (transmitting): ~200-500mA @ 5V
  - PSM (deep sleep): ~3-15µA
  - eDRX (light sleep): ~0.5-10mA
- **IP Rating**: IP65 or higher (weatherproof enclosure)
- **Mounting**: Weatherproof enclosure on tower equipment cabinet or shelter
- **Lightning Protection**: Surge protection required for outdoor installation
- **EMI/RFI**: Shielding required due to proximity to high-power RF equipment
