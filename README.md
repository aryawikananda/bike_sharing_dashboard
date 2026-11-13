# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk melakukan analisis dan visualisasi data **Bike Sharing** menggunakan **Streamlit**. Project ini bertujuan untuk mengeksplorasi pola penggunaan sepeda berdasarkan berbagai faktor, seperti waktu, musim, kondisi cuaca, serta karakteristik penyewaan sepeda.

## 📁 Project Structure

Berikut merupakan struktur direktori project:

```text
bike_sharing_dashboard/
│
├── dashboard/
│   ├── bike_sharing_clean.csv  # Dataset hasil pembersihan
│   └── dashboard.py            # Source code aplikasi Streamlit
│
├── data/
│   ├── Readme.txt              # Informasi dataset
│   ├── day.csv                 # Dataset penyewaan sepeda harian
│   └── hour.csv                # Dataset penyewaan sepeda per jam
│
├── README.md                   # Dokumentasi project
├── notebook.ipynb              # Notebook eksplorasi dan analisis data
├── requirements.txt            # Daftar library yang dibutuhkan
└── url.txt                     # Referensi URL terkait project
```

## ⚙️ Installation & Setup

### 1. Clone Repository

Clone repository ini ke komputer lokal:

```bash
git clone <repository-url>
```

Masuk ke direktori project:

```bash
cd bike_sharing_dashboard
```

### 2. Setup Environment - Anaconda

Jika menggunakan Anaconda, buat environment baru dengan Python 3.12:

```bash
conda create --name bike-sharing python=3.12
```

Aktifkan environment:

```bash
conda activate bike-sharing
```

### 3. Setup Environment - Shell/Terminal

Jika menggunakan Python Virtual Environment, jalankan perintah berikut:

```bash
python -m venv .venv
```

Aktifkan virtual environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

Setelah environment aktif, install seluruh library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

## 🚀 Run Streamlit Dashboard

Pastikan seluruh dependencies sudah terinstall dan environment telah aktif.

Jalankan aplikasi Streamlit menggunakan perintah berikut dari direktori utama project:

```bash
streamlit run dashboard/dashboard.py
```

Setelah aplikasi berhasil dijalankan, dashboard dapat diakses melalui browser pada alamat:

```text
http://localhost:8501
```

## 📚 Dependencies

Project ini menggunakan beberapa library Python berikut:

| Library | Kegunaan |
|---|---|
| **Streamlit** | Membangun dashboard interaktif. |
| **Pandas** | Melakukan pengolahan dan analisis data. |
| **NumPy** | Melakukan operasi numerik. |
| **Matplotlib** | Membuat visualisasi data. |
| **Seaborn** | Membuat visualisasi statistik. |
| **Plotly** | Membuat visualisasi data interaktif. |

## 📊 Project Overview

Dashboard ini menyajikan visualisasi dan analisis data Bike Sharing untuk membantu memahami pola penyewaan sepeda berdasarkan beberapa aspek, antara lain:

- **Temporal Analysis:** Analisis penggunaan sepeda berdasarkan waktu.
- **Seasonal Analysis:** Analisis pola penyewaan berdasarkan musim.
- **Weather Analysis:** Analisis hubungan kondisi cuaca dengan jumlah penyewaan sepeda.
- **User Behavior:** Eksplorasi karakteristik dan pola perilaku pengguna sepeda.

---

**Developed by:** Arya Wikananda