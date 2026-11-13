# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk melakukan analisis dan visualisasi data **Bike Sharing** menggunakan **Streamlit**. Dashboard ini menyajikan informasi mengenai pola penggunaan sepeda berdasarkan waktu, musim, kondisi cuaca, serta beberapa faktor lainnya.

## Setup Environment - Anaconda

```bash
conda create --name bike-sharing python=3.12
conda activate bike-sharing
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard

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

Kemudian install seluruh library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

## Run Streamlit App

Pastikan virtual environment sudah aktif, kemudian jalankan perintah berikut:

```bash
streamlit run dashboard.py
```

## Dependencies

Project ini menggunakan beberapa library Python berikut:

- **Streamlit** — membuat dashboard interaktif.
- **Pandas** — melakukan pengolahan dan analisis data.
- **NumPy** — melakukan operasi numerik.
- **Matplotlib** — membuat visualisasi data.
- **Seaborn** — membuat visualisasi statistik.
- **Plotly** — membuat visualisasi data interaktif.
