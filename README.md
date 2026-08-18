# 🇲🇾 Pusat Kawalan Bencana Negara (NDCC) | Malaysia Flood Telemetry Dashboard

A real-time National Disaster & Flood Telemetry Command Center dashboard across Malaysia. Built with **100% Pure Python** using **Plotly Dash**, **Plotly**, and **Pandas**, powered by official open telemetry data from [**api.data.gov.my/flood-warning/**](https://api.data.gov.my/flood-warning/) (Department of Irrigation and Drainage Malaysia / NADMA).

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-flood--warning--nadma.onrender.com-00c853?style=for-the-badge)](https://flood-warning-nadma.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.14-slate?style=for-the-badge&logo=plotly)](https://dash.plotly.com/)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Passing-success?style=for-the-badge&logo=githubactions)](https://github.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-00f0ff?style=for-the-badge&logo=render)](https://render.com/)

🔗 **Live Production URL:** [https://flood-warning-nadma.onrender.com/](https://flood-warning-nadma.onrender.com/)

---

## 🌟 Key Features

* **🇲🇾 Official NADMA Command Center Aesthetics**: Designed according to National Disaster Management Agency (NADMA) & JPS visual standards, incorporating official Jalur Gemilang vector emblem, corporate `Plus Jakarta Sans` typography, and `Roboto Mono` tabular figures.
* **🐍 100% Pure Python Stack**: No Node.js, npm, or frontend JavaScript builds required. Entirely powered by Plotly Dash, Gunicorn, and pure CSS.
* **🔒 Security Posture & Input Sanitization**: Secure HTTPS headers, regex input sanitization on filter callbacks to prevent injection vulnerabilities, and audit telemetry logging.
* **⚡ API Rate-Limit Resilience**: Graceful error handling for HTTP 429 rate limits, serving pre-structured fallback schemas to keep the interface 100% operational without crashing.
* **🚨 Real-Time Operational Alert Ticker**: Dynamic banner displaying emergency status (DANGER evacuation warnings, WARNING readiness alerts, or NORMAL status).
* **🗺️ Interactive Geospatial Radar Map**: Displays 1,276+ telemetry stations across Malaysia, color-coded by alert level (DANGER, WARNING, ALERT, NORMAL).
* **📊 Telemetry KPI Gauges**: Automatic station telemetry metrics with percentage ratios and disaster response directives.
* **📈 Threshold & Rainfall Intensity Analytics**:
  * Top 10 critical stations closest to or exceeding danger threshold levels.
  * Bullet / Gauge chart for station-specific water level threshold analysis.
  * Maximum daily rainfall intensity bar chart by state.
* **📋 Data Table & Audit CSV Export**: Complete telemetry station directory featuring native column search, sorting, and one-click CSV export.
* **⏱️ Keep-Alive Uptime Automation**: Built-in GitHub Actions scheduled workflow to prevent Render Free-tier cold starts.

---

## 📁 Project File Structure

```text
flood-warning/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml          # Automated CI/CD pipeline (Lint, Test, Auto-Deploy)
│       └── keep-alive.yml     # Scheduled cron pinger (prevents Render spindown)
├── app.py                     # Main entry point (Dash layout, callbacks & security)
├── data_loader.py             # Secure API fetcher & fallback loader (data.gov.my)
├── components/                # Modular Command Center Components
│   ├── navbar.py              # NDCC Header with Jalur Gemilang badge & security tags
│   ├── kpi_cards.py           # Summary telemetry gauge cards
│   ├── map_chart.py           # Interactive Plotly Carto-Darkmatter map
│   ├── analytics_charts.py    # Threshold comparison & gauge charts
│   └── data_table.py          # Telemetry matrix data table with CSV export
├── assets/
│   └── custom.css             # NADMA Slate Navy theme & typography rules
├── tests/
│   └── test_dashboard.py      # Automated Pytest suite with requests_mock
├── scripts/
│   └── local_test.sh          # Local pre-push test script
├── docs/
│   ├── SDD.md                 # System Design Document (Architecture & CI/CD)
│   ├── DEPLOYMENT.md          # Cloud deployment guide
│   └── RENDER_DEPLOYMENT.md   # Render.com deployment instructions
├── render.yaml                # Render 1-click cloud deployment manifest
├── Dockerfile                 # Production Docker container setup
├── Procfile                   # Gunicorn WSGI configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 💻 1. Installation & Local Setup

### Prerequisites
Ensure you have **Python 3.9+** installed on your system. (No Node.js needed).

### Step-by-Step Setup:
1. **Clone or navigate to the repository**:
   ```bash
   cd flood-warning
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run unit test suite**:
   ```bash
   pytest tests/ -v
   ```

4. **Start the application locally**:
   ```bash
   python app.py
   ```

5. **Open in Browser**:
   Navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050).

---

## 🚀 2. Deployment on Render

This repository is pre-configured with [`render.yaml`](render.yaml) and [`Procfile`](Procfile) for seamless deployment.

### Live URL:
👉 **[https://flood-warning-nadma.onrender.com/](https://flood-warning-nadma.onrender.com/)**

### Configuration:
* **Environment**: `Python 3.11`
* **Build Command**: `pip install -r requirements.txt`
* **Start Command**: `gunicorn app:server`

### 🔄 Keeping the Free-Tier Render App Alive
Render free-tier instances enter sleep mode after 15 minutes of inactivity. To ensure zero cold-start delay, this project utilizes **GitHub Actions Keep-Alive** ([`.github/workflows/keep-alive.yml`](.github/workflows/keep-alive.yml)) to ping the endpoint every 14 minutes:

```yaml
on:
  schedule:
    - cron: '*/14 * * * *'  # Runs ping every 14 minutes
```

---

## 🛠️ Tech Stack & Dependencies

| Tool / Library | Purpose |
| :--- | :--- |
| **Python 3.11** | Core Programming Language |
| **Dash (2.14+)** | Fullstack Web & UI Framework |
| **Dash Bootstrap Components** | Responsive UI Layout & Components |
| **Plotly (5.18+)** | Interactive Geospatial & Analytical Visualizations |
| **Pandas (2.0+)** | High-performance Telemetry Data Processing |
| **Requests** | Open API Consumer with Fallback Caching |
| **Gunicorn** | Production WSGI HTTP Server |
| **Pytest & Requests-Mock** | Automated Unit & Integration Testing Suite |
| **GitHub Actions** | CI/CD Pipeline & Uptime Automation |

---

## 📜 Data Source & License

Telemetry data is provided open-access by the **Department of Irrigation and Drainage (JPS) Malaysia** & **National Disaster Management Agency (NADMA)** via the official portal [**data.gov.my**](https://data.gov.my).
