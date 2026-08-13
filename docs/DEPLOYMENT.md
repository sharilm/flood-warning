# ☁️ Panduan Deployment ke Cloud (Free Tier)

Dokumen ini mengandungi panduan langkah-demi-langkah untuk menyebarkan (*deploy*) aplikasi **Pusat Kawalan Bencana Negara (NDCC) / NADMA Malaysia Telemetry Dashboard** ke perkhidmatan *Cloud Hosting Free Tier*.

---

## 📋 Prasyarat Deployment

Sebelum memulakan, pastikan:
1. Kod aplikasi anda telah berada di repository **GitHub**.
2. Fail [**`render.yaml`**](file:///Users/msharil/Devapp/antigravity/flood-warning/render.yaml), [**`Procfile`**](file:///Users/msharil/Devapp/antigravity/flood-warning/Procfile) dan [**`requirements.txt`**](file:///Users/msharil/Devapp/antigravity/flood-warning/requirements.txt) sedia ada.

---

## 🌐 Pilihan 1: Render.com (Paling Disyorkan ⭐)

**Render** menyediakan cloud hosting percuma untuk aplikasi Python Web Service. Rujuk panduan terperinci di [**`docs/RENDER_DEPLOYMENT.md`**](file:///Users/msharil/Devapp/antigravity/flood-warning/docs/RENDER_DEPLOYMENT.md).

### Ringkasan Langkah:
1. Push kod projek ini ke **GitHub** anda.
2. Daftar akaun percuma di [Render.com](https://render.com/).
3. Di Dashboard Render, klik **New +** ➡️ pilih **Web Service**.
4. Sambungkan akaun GitHub anda dan pilih repository `flood-warning`. Render akan mengesan `render.yaml` secara automatik.
5. Isikan tetapan berikut:
   * **Name**: `flood-warning-nadma`
   * **Region**: *Singapore (ap-southeast-1)*
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:server`
   * **Instance Type**: `Free`
6. Klik **Create Web Service**. URL percuma anda akan diberikan (contoh: `https://flood-warning-nadma.onrender.com`).

---

## 🚀 Pilihan 2: Koyeb (Percuma & Pantas)

[Koyeb](https://www.koyeb.com/) menawarkan perkhidmatan cloud percuma dengan 512MB RAM & pemprosesan pantas.

### Langkah-langkah:
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

## 🤗 Pilihan 3: Hugging Face Spaces (Percuma)

1. Log masuk ke [Hugging Face](https://huggingface.co/) dan cipta **Space Baru**.
2. Pilih SDK **Docker**.
3. Muat naik fail repo (termasuk `Dockerfile`).

---

## 🐍 Pilihan 4: PythonAnywhere (Percuma)

1. Daftar akaun percuma di [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Di tab **Bash**, clone repo anda & install requirements.
3. Di tab **Web**, tetapkan arahan WSGI ke `from app import server as application`.
