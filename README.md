# simple-lms

Aplikasi Flask sederhana dengan endpoint health check dan penghitung kunjungan
yang disimpan di Redis. Docker Compose menjalankan aplikasi, Redis, dan
PostgreSQL.

## Prasyarat

- Docker Desktop dengan Docker Compose
- Atau Python 3.12 dan Redis jika ingin menjalankan aplikasi secara lokal

## Menjalankan dengan Docker Compose

1. Dari folder project, buat file `.env` dengan konfigurasi berikut:

   ```dotenv
   POSTGRES_DB=simple_lms
   POSTGRES_USER=lms_user
   POSTGRES_PASSWORD=ubah_password_ini
   REDIS_HOST=redis
   PGADMIN_DEFAULT_EMAIL=admin@example.com
   ```

   Nilai PostgreSQL diperlukan oleh image PostgreSQL. Aplikasi saat ini
   menggunakan Redis dan belum terhubung ke PostgreSQL. Email pgAdmin
   digunakan untuk login ke antarmuka web; password-nya secara default sama
   dengan `POSTGRES_PASSWORD`. Untuk menggunakan password berbeda, tambahkan
   `PGADMIN_DEFAULT_PASSWORD=kata_sandi_kuat` ke `.env`.

2. Jalankan layanan:

   ```powershell
   docker compose up -d --remove-orphans
   ```

3. Buka `http://localhost:8000/health` untuk memeriksa status aplikasi.
   Endpoint `http://localhost:8000/` mengembalikan nama service dan jumlah
   kunjungan, yang bertambah setiap kali endpoint tersebut dipanggil.

## Membuka PostgreSQL dengan pgAdmin

1. Buka `http://localhost:5050` di browser.
2. Login dengan email `PGADMIN_DEFAULT_EMAIL` dan password
   `PGADMIN_DEFAULT_PASSWORD` dari file `.env`. Jika variabel password itu
   belum ditambahkan, gunakan nilai `POSTGRES_PASSWORD`.
3. Pilih **Add New Server**. Pada tab **General**, isi nama server, misalnya
   `Project DB`.
4. Pada tab **Connection**, isi:
   - **Host name/address:** `db`
   - **Port:** `5432`
   - **Maintenance database:** nilai `POSTGRES_DB` dari `.env`
   - **Username** dan **Password:** nilai `POSTGRES_USER` dan
     `POSTGRES_PASSWORD` dari `.env`
5. Simpan koneksi. Database akan muncul di panel navigasi pgAdmin.

Gunakan host `db` karena pgAdmin berjalan di dalam jaringan Docker Compose.
pgAdmin menyimpan pengaturan koneksi pada volume `pgadmin_data`.

Untuk melihat log:

```powershell
docker compose logs -f app
```

Untuk menghentikan layanan:

```powershell
docker compose down
```

Data PostgreSQL dan Redis disimpan di Docker volumes. Untuk menghapus layanan
beserta data volumes, jalankan `docker compose down -v`.

## Menjalankan secara lokal

Pastikan Redis sudah berjalan dan dapat diakses. Dari PowerShell di folder
project, buat virtual environment, aktifkan, lalu pasang dependensi:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:REDIS_HOST = "localhost"
python app.py
```

Aplikasi berjalan di `http://localhost:5000`. Jika kebijakan PowerShell
mencegah aktivasi virtual environment, jalankan Python dari environment
tersebut secara langsung:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:REDIS_HOST = "localhost"
.\.venv\Scripts\python.exe app.py
```

## Endpoint

| Method | Path | Keterangan |
| --- | --- | --- |
| `GET` | `/` | Mengembalikan `service` dan jumlah kunjungan dari Redis |
| `GET` | `/health` | Mengembalikan status kesehatan aplikasi |

Jangan gunakan nilai contoh `POSTGRES_PASSWORD` di atas untuk deployment
produksi.
