# 🇲🇾 Pusat Kawalan Bencana Negara (NDCC) | Malaysia Flood Telemetry Dashboard

A real-time National Disaster & Flood Telemetry Command Center dashboard across Malaysia. Built using **Python Dash**, **Plotly**, and **Pandas**, powered by official open telemetry data from [**api.data.gov.my/flood-warning/**](https://api.data.gov.my/flood-warning/) (Department of Irrigation and Drainage Malaysia / NADMA).

![Dashboard Status](https://img.shields.io/badge/Status-Live_NDCC-0284c7?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python) ![Dash](https://img.shields.io/badge/Dash-2.14-slate?style=for-the-badge) ![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Passing-success?style=for-the-badge&logo=githubactions) ![Render Deployment](https://img.shields.io/badge/Render-Ready-00f0ff?style=for-the-badge)

---

## 🌟 Key Features

* **🇲🇾 Official NADMA Government Command Center Aesthetics**: Designed according to National Disaster Management Agency (NADMA) & JPS visual standards, incorporating official Jalur Gemilang vector emblem, corporate `Plus Jakarta Sans` typography, and `Roboto Mono` tabular figures.
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

---

## 📁 Project File Structure

```text
flood-warning/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Automated GitHub Actions CI/CD pipeline
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
Ensure you have **Python 3.9+** installed on your system.

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
   pytest tests/
   ```

4. **Start the application**:
   ```bash
   python app.py
   ```

5. **Open in Browser**:
   Navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050).

---

## 🚀 2. Deployment to Render

This project includes a pre-configured `render.yaml` and `Procfile` for seamless deployment on **Render**.

1. Push your latest code to GitHub:
   ```bash
   git push origin main
   ```
2. Log into [dashboard.render.com](https://dashboard.render.com).
3. Select **New +** → **Web Service**.
4. Connect your GitHub repository. Render will automatically detect `render.yaml`:
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:server`

---

## 🛠️ Tech Stack & Dependencies

* `dash` — Core Web Application Framework
* `dash-bootstrap-components` — Responsive Grid System & UI Components
* `plotly` — Interactive Mapbox & Data Visualization
* `pandas` — Telemetry Data Processing & Wrangling
* `requests` — Secure HTTP Client for data.gov.my OpenAPI
* `gunicorn` — Production WSGI HTTP Server
* `pytest` & `requests_mock` — Automated Unit Testing

---

## 📜 Data Source & License

Telemetry data is provided open-access by the **Department of Irrigation and Drainage (JPS) Malaysia** & **National Disaster Management Agency (NADMA)** via official portal [**data.gov.my**](https://data.gov.my).
