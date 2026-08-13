# 🌊 Malaysia Flood Warning Center (MY Flood Warning Dashboard)

A real-time river water level and flood warning monitoring dashboard across Malaysia. Built using **Python Dash**, **Plotly**, and **Pandas**, powered by open telemetry data from [**api.data.gov.my/flood-warning/**](https://api.data.gov.my/flood-warning/).

![Dashboard Preview](https://img.shields.io/badge/Status-Live-emerald?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python) ![Dash](https://img.shields.io/badge/Dash-2.14-slate?style=for-the-badge) ![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Passing-success?style=for-the-badge&logo=githubactions) ![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)

---

## 🌟 Key Features

* **🗺️ Interactive Geospatial Map**: Displays 1,276+ telemetry stations across Malaysia, color-coded by alert status (Normal, Alert, Warning, Danger).
* **📊 Status KPI Cards**: Automatic station counts categorized into **DANGER**, **WARNING**, **ALERT**, and **NORMAL**.
* **🎯 Dynamic Filters**: Multi-criteria filtering by State, District, Alert Level, and text search by station or river name.
* **📈 Threshold & Rainfall Analytics**:
  * Top 10 stations closest to or exceeding danger threshold levels.
  * Interactive Bullet / Gauge Chart for selected telemetry stations.
  * Maximum daily rainfall bar chart grouped by state.
* **📋 Data Table & CSV Export**: Complete telemetry station directory featuring native column search, sorting, and one-click CSV export.
* **🔄 Automatic Live Updates**: Automatically refreshes live API data every 10 minutes (or via manual *Refresh* button).

---

## 📁 Project File Structure

```text
flood-warning/
├── .github/
│   └── workflows/
│       └── ci-cd.yml   # Automated GitHub Actions CI/CD pipeline
├── app.py              # Main entry point (Dash app & callbacks)
├── data_loader.py      # API fetch & data cleaning module (data.gov.my)
├── components/         # Modular UI Components
│   ├── navbar.py           # Header with live status badge & refresh button
│   ├── kpi_cards.py        # Summary KPI cards
│   ├── map_chart.py        # Interactive Plotly Carto-Darkmatter map
│   ├── analytics_charts.py # Threshold comparison & gauge charts
│   └── data_table.py       # Data table with CSV export
├── assets/
│   └── custom.css      # Dark Slate theme styling & CSS animations
├── tests/
│   └── test_dashboard.py # Automated Pytest unit test suite
├── scripts/
│   └── local_test.sh   # Local pre-push lint & test script
├── Dockerfile          # Production Docker container setup
├── .dockerignore       # Docker ignore rules
├── Procfile            # Gunicorn WSGI configuration for production
├── requirements.txt    # Python dependencies list
└── README.md           # Project documentation & instructions
```

---

## 💻 1. Installation & Local Setup

### Prerequisites
Make sure you have **Python 3.9+** installed on your system.

### Step-by-step Setup:
1. **Clone or navigate to the repository**:
   ```bash
   cd flood-warning
   ```

2. **Install required Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run local pre-push tests (Optional)**:
   ```bash
   ./scripts/local_test.sh
   # or: pytest tests/
   ```

4. **Start the application**:
   ```bash
   python app.py
   ```

5. **Open in Browser**:
   Navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050) or [http://localhost:8050](http://localhost:8050).

---

## 🔄 2. CI/CD Pipeline (GitHub Actions)

This repository includes an automated **GitHub Actions** workflow defined in `.github/workflows/ci-cd.yml`.

* **CI (Continuous Integration)**: Triggered on every `push` or `pull_request` to the `main` branch:
  * Runs Python syntax & linting checks (`flake8`).
  * Runs automated unit & UI component tests (`pytest tests/`).
* **CD (Continuous Deployment)**: Triggers an automated *Deploy Webhook* to your cloud provider (e.g., Render or Koyeb) once CI tests pass.

---

## 🛠️ Tech Stack & Dependencies

* `dash` — Core Web Framework
* `dash-bootstrap-components` — Responsive Grid System & Bootstrap Components
* `plotly` — Interactive Carto Mapbox & Analytics Charts
* `pandas` — Data Wrangling & Manipulation
* `requests` — HTTP Client for data.gov.my OpenAPI
* `gunicorn` — Production WSGI HTTP Server
* `pytest` & `flake8` — Automated Testing & Code Quality Tools

---

## 📜 Data Source & License

Telemetry data is provided open-access by the **Department of Irrigation and Drainage (JPS) Malaysia** via the official portal [**data.gov.my**](https://data.gov.my).
