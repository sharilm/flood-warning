# 🚀 Panduan Deployment Rasmi ke Render.com

Panduan ini menerangkan langkah-demi-langkah cara menyebarkan (*deploy*) aplikasi **Pusat Kawalan Bencana Negara (NDCC) / NADMA Malaysia Telemetry Dashboard** ke **Render.com** secara percuma.

---

## 📋 Prasyarat

Sebelum memulakan deployment, pastikan fail-fail berikut sedia ada di dalam repositori anda:
- [**`render.yaml`**](file:///Users/msharil/Devapp/antigravity/flood-warning/render.yaml) — Fail manifest penemuan automatik Render.
- [**`Procfile`**](file:///Users/msharil/Devapp/antigravity/flood-warning/Procfile) — Mengandungi arahan pelancaran `web: gunicorn app:server`.
- [**`requirements.txt`**](file:///Users/msharil/Devapp/antigravity/flood-warning/requirements.txt) — Senarai pakej Python termasuk `gunicorn`, `dash`, `plotly`, `pandas`, `requests`.

---

## 🛠️ Langkah-Langkah Deployment (1-Click Blueprint)

### Langkah 1: Push Kod ke GitHub
Muat naik sebarang perubahan kod terbaharu ke repositori GitHub anda:
```bash
git add .
git commit -m "build: ready for Render deployment"
git push origin main
```

### Langkah 2: Log Masuk ke Render
1. Layari **[dashboard.render.com](https://dashboard.render.com/)**.
2. Log masuk menggunakan akaun GitHub anda.

### Langkah 3: Cipta Web Service Baru
1. Klik butang **"New +"** di sudut kanan atas → pilih **"Web Service"**.
2. Pilih **"Build and deploy from a Git repository"** dan klik **Next**.
3. Pilih repositori `flood-warning` anda dari senarai repositori GitHub.

### Langkah 4: Tetapan Web Service
Render akan mengesan fail `render.yaml` secara automatik. Sekiranya anda membuat tetapan manual, isikan maklumat seperti berikut:

| Parameter | Nilai Tetapan |
| :--- | :--- |
| **Name** | `flood-warning-nadma` *(atau nama pilihan anda)* |
| **Region** | `Singapore (ap-southeast-1)` *(Disyorkan untuk Malaysia)* |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:server` |
| **Instance Type** | `Free` |

### Langkah 5: Pelancaran (*Deploy*)
1. Klik butang **"Create Web Service"**.
2. Render akan mula memuat turun pakej dan membina aplikasi (mengambil masa sekitar 1–2 minit).
3. Setelah status bertukar ke **Live**, anda akan menerima pautan HTTPS percuma, contohnya:
   ```text
   https://flood-warning-nadma.onrender.com
   ```

---

## 🔄 Persediaan Auto-Deploy Webhook (GitHub Actions)

Untuk membolehkan Render mengemaskini deployment secara automatik setiap kali anda membuat `git push origin main`:

1. Di **Render Dashboard** → Buka Web Service anda → **Settings** → Salin URL di bahagian **Deploy Hook**.
2. Di **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**.
3. Tambah Secret Baru:
   * **Name**: `RENDER_DEPLOY_HOOK_URL`
   * **Value**: *[Tampal Deploy Hook URL dari Render]*
4. GitHub Actions dalam `.github/workflows/ci-cd.yml` akan secara automatik memicu deployment Render sebaik sahaja semua ujian unit (`pytest`) lulus.

---

## ❓ Penyelesaian Masalah (Troubleshooting)

* **Ralat `Port in use`**: Render mengendalikan penetapan `PORT` secara automatik melalui persekitaran `gunicorn app:server`.
* **Ralat `429 Too Many Requests`**: Aplikasi sudah dilengkapi dengan *fallback schema* automatik dalam `data_loader.py` supaya paparan tidak terhempas jika REST API data.gov.my mempunyai had permintaan sementara.
