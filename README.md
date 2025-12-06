# 🎓 Smart Campus Scheduler (AI Based)

**Sistem Penjadwalan Mata Kuliah Otomatis** berbasis **Algoritma Genetika (Genetic Algorithm)**.

Aplikasi web modern ini dibangun menggunakan **Python (Flask)** dan **MySQL**, dirancang untuk menyelesaikan masalah kompleks penjadwalan kampus (bentrok dosen, kapasitas ruangan, jenis laboratorium, dan beban SKS) secara otomatis dengan hasil yang optimal.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

---

## ✨ Fitur Utama

* **🧠 Algoritma Genetika Cerdas:**
    * Mencegah bentrok jadwal Dosen & Ruangan
    * Validasi Kapasitas Ruangan vs Jumlah Mahasiswa
    * Validasi Jenis Ruangan (Praktikum wajib di Lab)
    * Mencegah tabrakan mata kuliah di Semester yang sama
* **📂 Hybrid Upload:** Mendukung upload data via **Excel (Single File)** yang praktis atau **CSV (Terpisah)**
* **📥 Template Generator:** Fitur download template Excel/CSV langsung dari dashboard agar format data selalu benar
* **📊 Interactive Dashboard:** Menampilkan statistik jumlah mata kuliah, dosen, ruangan, dan total beban SKS
* **⚠️ Detail Konflik:** Laporan mendalam mengenai letak kesalahan jadwal (misal: "Dosen A bentrok di Slot 5")
* **📄 PDF Export:** Unduh hasil jadwal yang sudah jadi ke dalam format PDF siap cetak
* **👨‍🏫 Monitoring Dosen:** Fitur untuk melihat beban kerja dosen (Underload / Ideal / Overload)

---

## 🛠️ Prasyarat (Requirements)

Sebelum menjalankan aplikasi, pastikan laptop Anda sudah terinstall:

1. **Python 3.x** (Disarankan Python 3.10 ke atas)
2. **XAMPP** (Untuk database MySQL/MariaDB)
3. **Git** (Opsional, untuk clone repository)
4. **Web Browser** Modern (Chrome, Edge, Firefox)

---

## 🚀 Panduan Instalasi (Step-by-Step)

Ikuti langkah-langkah ini di Terminal / Command Prompt (CMD) / PowerShell.

### 1. Clone atau Download Project

```bash
git clone https://github.com/adityaalfandy/smart_scheduler
cd smart-scheduler
```

(Jika mendownload ZIP, ekstrak filenya lalu buka folder tersebut di VS Code / Terminal)

### 2. Buat Virtual Environment (Disarankan)

Supaya library Python tidak tercampur dengan project lain.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Library Python

Install semua dependensi yang dibutuhkan.

```bash
pip install -r requirements.txt
```


### 4. Setup Database (XAMPP)

1. Buka aplikasi **XAMPP Control Panel**
2. Klik tombol **Start** pada modul **Apache** dan **MySQL**
3. Buka browser dan akses: `http://localhost/phpmyadmin`
4. Klik tab **SQL**, lalu jalankan perintah ini untuk membuat database baru:

```sql
CREATE DATABASE smart_scheduler_db;
```

(Tabel-tabel di dalamnya akan dibuat otomatis oleh Python saat aplikasi dijalankan pertama kali)

### 5. Jalankan Aplikasi

Kembali ke terminal proyek Anda, jalankan perintah:

```bash
python app.py
```

Jika berhasil, akan muncul tulisan seperti: `Running on http://127.0.0.1:5000`

---

## 📖 Cara Penggunaan

1. **Buka Website:** Buka browser dan akses alamat `http://127.0.0.1:5000`

2. **Download Template:**
   - Di Dashboard, klik tombol "⬇ Template Excel"
   - File `Template_Lengkap.xlsx` akan terunduh

3. **Isi Data:**
   - Buka file Excel tersebut
   - Isi Sheet **Matkul** (Kode MK, Dosen, Slot Waktu, dll)
   - Isi Sheet **Ruangan** (Nama Ruang, Kapasitas, Jenis)
   - **Tips:** Gunakan kode slot waktu 1-40 (Lihat menu "Panduan" di pojok kanan atas website)

4. **Upload Data:**
   - Kembali ke website, pilih tab **Import Excel**
   - Upload file yang sudah diisi tadi

5. **Generate Jadwal:**
   - Klik tombol **🚀 GENERATE JADWAL**
   - Tunggu proses optimasi (biasanya 10-60 detik tergantung jumlah data)

6. **Lihat Hasil:**
   - Jika sukses, tabel jadwal akan muncul
   - Jika ada konflik, klik tombol "Sisa Konflik" untuk melihat detail masalahnya
   - Klik **Download PDF** untuk menyimpan laporan

---

## 📂 Struktur Project

```
smart_scheduler/
│
├── app.py                   # File Utama (Server Flask & Konfigurasi)
├── requirements.txt         # Daftar Library Python
├── static/                  # Folder aset statis
│   └── schedule_report.pdf  # Hasil generate PDF
│
├── templates/               # Folder HTML (Frontend)
│   ├── layout.html          # Template Induk (Sidebar & Header)
│   ├── index.html           # Halaman Dashboard & Upload
│   ├── result.html          # Halaman Hasil Jadwal
│   └── dosen.html           # Halaman Monitoring Dosen
│
└── app/                     # Modul Logika (Backend AI)
    └── genetic_algorithm/   # Folder Core Algoritma Genetika
        ├── __init__.py
        ├── population.py    # Manajemen Populasi
        ├── chromosome.py    # Struktur Data Gen/Kromosom
        ├── fitness.py       # Fungsi Penilaian (Score & Konflik)
        ├── crossover.py     # Logika Kawin Silang
        ├── mutation.py      # Logika Mutasi
        └── selection.py     # Logika Seleksi Turnamen
```

---

## ❓ Troubleshooting (Masalah Umum)

### 🔴 Error: "Can't connect to MySQL server"
**Penyebab:** Database MySQL belum menyala.

**Solusi:** Buka XAMPP, pastikan modul MySQL sudah di-Start (berwarna hijau).

### 🔴 Error: "ModuleNotFoundError"
**Penyebab:** Library Python belum terinstall.

**Solusi:** Jalankan `pip install -r requirements.txt` di terminal.

### 🔴 Error saat Upload Excel
**Penyebab:** Format Excel salah atau nama Sheet tidak sesuai.

**Solusi:** Pastikan file Excel memiliki 2 Sheet dengan nama persis: **Matkul** dan **Ruangan**. Gunakan fitur "Download Template" di dashboard agar aman.

### 🔴 Hasil Jadwal Masih Banyak Konflik
**Penyebab:** Data terlalu ketat (Ruangan kurang atau Waktu Dosen terlalu sempit).

**Solusi:**
- Tambah jumlah ruangan atau kapasitasnya
- Perbanyak slot waktu tersedia bagi dosen
- Naikkan parameter `generations` atau `population_size` di file `app.py`

---

## 👨‍💻 Kontributor

Dibuat dengan ❤️ untuk mempermudah proses penjadwalan akademik kampus.

---


---

## 🙏 Dukungan

Jika project ini membantu Anda, berikan ⭐ **Star** di GitHub!

Untuk pertanyaan atau bug report, silakan buka **Issues** di repository ini.
