# AIHackathon2025_AIBuoy_SmartBuoy_Backend

A lightweight backend service that collects, processes, and stores sensor data from a network of smart buoys. Buoys form a LoRa mesh to relay measurements offshore to a central gateway, which forwards data to this server for validation, storage, and alerting.

---

## Features

- LoRa-based mesh network between buoys for low-power, long-range communication  
- Central gateway buoy that uplinks aggregated data via cellular or satellite  
- REST API for buoy registration, status checks, and data ingestion  
- Real-time validation and normalization of sensor payloads  
- Time-series storage in InfluxDB and metadata in PostgreSQL  
- Threshold-based alerts delivered via webhooks or email notifications  

---

## Architecture Overview

```text
   ┌────────────┐          LoRa Mesh         ┌──────────────┐
   │  Buoy A    │─────────▶ Buoy B ─────────▶ Buoy C (GW) │
   │(Sensors)   │          ▲      ▼          │(Gateway)    │
   └────────────┘          │      │          └───────┬────┘
                           │      │                  │
                           ▼      └──────────────────┘
                      ┌─────────────────────────────────────┐
                      │  Offshore Server (Backend API)      │
                      │                                     │
                      │  • Data validation & enrichment    │
                      │  • Time-series storage (InfluxDB)   │
                      │  • Metadata storage (PostgreSQL)    │
                      │  • Alerting & webhook dispatch      │
                      └─────────────────────────────────────┘
```

---

## Getting Started

1. Clone the repository  
   ```bash
   git clone https://github.com/your-org/AIHackathon2025_AIBuoy_SmartBuoy_Backend.git
   cd AIHackathon2025_AIBuoy_SmartBuoy_Backend
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in a `.env` file based on `.env.example`  

4. Launch with Docker Compose  
   ```bash
   docker-compose up -d
   ```

---

## Usage

- Register a new buoy  
  `POST /api/v1/buoy/register`  

- Send sensor data  
  `POST /api/v1/data`  

- Fetch buoy status  
  `GET /api/v1/buoy/{id}/status`  

- Query stored measurements  
  `GET /api/v1/data?from=<ts>&to=<ts>`  

---

## License

This project is licensed under the MIT License.
