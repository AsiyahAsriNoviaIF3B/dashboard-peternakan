# Dashboard Visualisasi Data Peternakan

Aplikasi Streamlit untuk praktikum visualisasi data sektor peternakan. Aplikasi ini menggunakan data simulasi yang dibuat di dalam `app.py`; data bukan data lapangan/riil.

## Jalankan di komputer sendiri untuk pengujian

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Publikasikan ke internet

1. Buat repository baru di GitHub.
2. Unggah `app.py` dan `requirements.txt` ke root repository.
3. Buka https://share.streamlit.io/ dan masuk menggunakan GitHub.
4. Pilih **Create app**, kemudian pilih repository, branch (biasanya `main`), dan file utama `app.py`.
5. Tentukan subdomain bila tersedia, lalu klik **Deploy**.
6. Setelah proses selesai, buka URL `https://nama-aplikasi.streamlit.app` yang dibuat oleh Streamlit.
7. Di bagian Settings/Sharing, pastikan akses diatur menjadi publik bila aplikasi akan dinilai dosen melalui tautan.

## Mengganti data simulasi dengan CSV asli

Untuk tugas yang memakai data asli, tambahkan CSV ke repository atau sediakan uploader CSV pada aplikasi, lalu sesuaikan nama kolom dengan kolom yang digunakan di `app.py`. Jangan menyajikan data simulasi sebagai data lapangan.
