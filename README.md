# 🌊 Pusat Amaran Banjir Malaysia (MY Flood Warning Dashboard)

Dashboard pemantauan paras air sungai dan amaran banjir real-time seluruh Malaysia. Dibina menggunakan **Python Dash**, **Plotly**, dan **Pandas** berasaskan data OpenAPI daripada [**api.data.gov.my/flood-warning/**](https://api.data.gov.my/flood-warning/).

![Dashboard Preview](https://img.shields.io/badge/Status-Live-emerald?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python) ![Dash](https://img.shields.io/badge/Dash-2.14-slate?style=for-the-badge) ![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Passing-success?style=for-the-badge&logo=githubactions) ![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)

---

## 🌟 Ciri-Ciri Utama

* **🗺️ Peta Interaktif Geospatial**: Menunjukkan 1,276+ lokasi stesen telemetri di seluruh Malaysia dengan kod warna mengikut paras amaran.
* **📊 Kad KPI Ringkasan Status**: Kiraan automatik stesen mengikut kategori **BAHAYA (DANGER)**, **AMARAN (WARNING)**, **WASPADA (ALERT)**, dan **NORMAL**.
* **🎯 Penapis Dinamik**: Tapisan mengikut Negeri, Daerah, Status Amaran, serta kotak carian nama stesen / sungai.
* **📈 Analisis Graf Ambang & Hujan**:
  * Top 10 stesen paling hampir atau melepasi aras bahaya.
  * Bullet / Gauge Chart mengikut stesen yang dipilih.
  * Graf bar rekod hujan maksimum mengikut negeri.
* **📋 Jadual Data & Eksport CSV**: Senarai penuh stesen dengan kebolehan carian, susunan (*sort*), dan butang muat turun fail CSV.
* **🔄 Kemaskini Automatik**: Mengemas kini data secara berkala setiap 10 minit (atau butang *Refresh Manual*).

---

## 📁 Struktur Fail Projek

```text
flood-warning/
├── .github/
│   └── workflows/
│       └── ci-cd.yml   # Workflow GitHub Actions untuk CI/CD automatik
├── app.py              # Main entry point (Dash app & callbacks)
├── data_loader.py      # Modul pengambil & pembersih data api.data.gov.my
├── components/         # Komponen UI Modular
│   ├── navbar.py           # Header & status live
│   ├── kpi_cards.py        # Kad ringkasan KPI
│   ├── map_chart.py        # Peta Plotly Carto-Darkmatter
│   ├── analytics_charts.py # Graf perbandingan & gauge threshold
│   └── data_table.py       # Jadual data & muat turun CSV
├── assets/
│   └── custom.css      # Styling tema Dark Slate & animasi
├── tests/
│   └── test_dashboard.py # Pytest unit test suite
├── scripts/
│   └── local_test.sh   # Skrip pengesahan & ujian tempatan
├── Dockerfile          # Tetapan kontena produksi Docker
├── .dockerignore       # Pengecualian fail Docker
├── Procfile            # Tetapan WSGI Gunicorn untuk Cloud Deployment
├── requirements.txt    # Pustaka Python yang diperlukan
└── README.md           # Dokumen projek & panduan deployment
```

---

## 💻 1. Cara Pemasangan & Larian Lokal (Local Setup)

### Prasyarat
Sila pastikan anda mempunyai **Python 3.9+** terpasang pada komputer anda.

### Langkah-langkah:
1. **Clone atau muat turun repository ini**:
   ```bash
   cd flood-warning
   ```

2. **Pasang pustaka Python yang diperlukan**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Ujian Tempatan (Optional)**:
   ```bash
   ./scripts/local_test.sh
   # atau: pytest tests/
   ```

4. **Jalankan aplikasi**:
   ```bash
   python app.py
   ```

5. **Buka di Penyemak Imbas (Browser)**:
   Layari [http://127.0.0.1:8050](http://127.0.0.1:8050) atau [http://localhost:8050](http://localhost:8050).

---

## 📤 2. Langkah Push Kod ke GitHub

Untuk memuat naik kod ini ke akaun GitHub anda:

```bash
# 1. Tambah semua fail ke git
git init
git add .

# 2. Buat commit
git commit -m "feat: MY Flood Warning Dashboard with CI/CD & Docker"

# 3. Hubungkan ke repository GitHub anda
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO-ANDA.git

# 4. Push ke GitHub
git push -u origin main
```

---

## 🔄 3. Pipeline CI/CD (GitHub Actions)

Repository ini dilengkapi alur kerja automatik **GitHub Actions** dalam `.github/workflows/ci-cd.yml`.

### Fungsi Automasi (CI/CD):
1. **CI (Continuous Integration)**: Setiap kali anda melakukan `git push` atau `pull request` ke cawangan `main`:
   * Mengesan ralat sintaks Python (`flake8`).
   * Menjalankan ujian unit & ujian komponen UI secara automatik (`pytest tests/`).
2. **CD (Continuous Deployment)**: Selepas ujian CI lulus:
   * Menghantar *Deploy Webhook* secara automatik ke **Render.com** atau **Koyeb** untuk mengemas kini aplikasi live anda tanpa sebarang klik manual.

### Cara Mengaktifkan Auto-Deploy Webhook di GitHub:
1. Di **Render.com Dashboard** ➡️ Buka Web Service anda ➡️ *Settings* ➡️ Salin **Deploy Hook URL**.
2. Di **GitHub Repository** anda ➡️ Buka **Settings** ➡️ **Secrets and variables** ➡️ **Actions**.
3. Klik **New repository secret**:
   * **Name**: `RENDER_DEPLOY_HOOK_URL`
   * **Value**: *[Tampal Deploy Hook URL dari Render]*
4. Setiap kali anda push kod baru (`git push origin main`), GitHub Actions akan secara automatik menguji kod dan mengarahkan Render/Koyeb mengemaskini deployment anda! 🚀

---

## ☁️ 4. Panduan Deploy ke Cloud (Free Tier)

Aplikasi ini bersedia untuk *deployment* kerana telah dieksport dengan WSGI Gunicorn (`server = app.server` dalam `app.py`) dan fail `Dockerfile`. Berikut ialah beberapa pilihan cloud percuma:

---

### 🌐 Pilihan A: Render.com (Paling Disyorkan ⭐)

**Render** menyediakan cloud hosting percuma untuk aplikasi Python (Web Service).

#### Langkah-langkah Deployment di Render:
1. Push kod projek ini ke **GitHub** anda.
2. Daftar akaun percuma di [Render.com](https://render.com/).
3. Di Dashboard Render, klik **New +** ➡️ pilih **Web Service**.
4. Sambungkan akaun GitHub anda dan pilih repository `flood-warning`.
5. Isikan tetapan berikut:
   * **Name**: `my-flood-warning`
   * **Region**: *Singapore (ap-southeast-1)*
   * **Runtime**: `Python 3` (atau `Docker`)
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:server`
   * **Instance Type**: `Free`
6. Klik **Create Web Service**. 
7. URL percuma anda akan diberikan (contoh: `https://my-flood-warning.onrender.com`).

---

### 🚀 Pilihan B: Koyeb (Percuma & Pantas)

[Koyeb](https://www.koyeb.com/) menawarkan perkhidmatan cloud percuma dengan 512MB RAM.

1. Push kod ke **GitHub**.
2. Log masuk ke [Koyeb Dashboard](https://app.koyeb.com/).
3. Klik **Create Service** ➡️ Pilih **GitHub**.
4. Pilih repository `flood-warning`.
5. Tetapkan:
   * **Builder**: `Dockerfile` atau `Buildpack`
   * **Run Command**: `gunicorn app:server --bind 0.0.0.0:8000`
   * **Port**: `8000`
6. Klik **Deploy**.

---

### 🤗 Pilihan C: Hugging Face Spaces (Percuma Tanpa Had Masa)

Hugging Face Spaces menyediakan hosting percuma CPU 16GB RAM.

1. Log masuk ke [Hugging Face](https://huggingface.co/) dan cipta **Space Baru**.
2. Pilih SDK **Docker**.
3. Muat naik semua fail repo (termasuk `Dockerfile`).
4. Space anda akan automatik terbina dan berjalan.

---

### 🐍 Pilihan D: PythonAnywhere (Percuma)

1. Daftar akaun percuma di [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Di tab **Bash**, clone repo anda:
   ```bash
   git clone https://github.com/USERNAME/flood-warning.git
   cd flood-warning
   pip install --user -r requirements.txt
   ```
3. Di tab **Web**, klik **Add a new web app** ➡️ Pilih **Manual Configuration (Python 3.11)**.
4. Pada bahagian **WSGI configuration file**, kemaskini kod WSGI kepada:
   ```python
   import sys
   path = '/home/YOUR_USERNAME/flood-warning'
   if path not in sys.path:
       sys.path.append(path)
   from app import server as application
   ```
5. Klik **Reload**.

---

## 🛠️ Pustaka & Dependencies

* `dash` — Framework UI Web
* `dash-bootstrap-components` — Grid system & tema Bootstrap
* `plotly` — Peta Mapbox & graf visualisasi interaktif
* `pandas` — Pemprosesan & analisis data
* `requests` — HTTP client untuk OpenAPI
* `gunicorn` — WSGI HTTP Server untuk pengeluaran (Production)
* `pytest` & `flake8` — Ujian automatik & pemantauan sintaks

---

## 📜 Lesen & Sumber Data

Data bersumberkan secara terbuka daripada **Jabatan Pengairan dan Saliran (JPS) Malaysia** melalui portal rasmi **[data.gov.my](https://data.gov.my)**.
