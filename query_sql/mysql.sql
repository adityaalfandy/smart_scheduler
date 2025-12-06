DROP DATABASE IF EXISTS smart_scheduler_db;

CREATE DATABASE smart_scheduler_db;


USE smart_scheduler_db;

CREATE TABLE ruangan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_ruangan VARCHAR(100) NOT NULL,
    kapasitas INT NOT NULL DEFAULT 40,
    jenis VARCHAR(50) NOT NULL DEFAULT 'Teori',
    fasilitas VARCHAR(255) DEFAULT 'Standard'
);

CREATE TABLE mata_kuliah (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_mk VARCHAR(50) NOT NULL,
    nama_mk VARCHAR(200) NOT NULL,
    sks INT NOT NULL DEFAULT 2,
    fakultas VARCHAR(100),
    dosen VARCHAR(150) NOT NULL,
    waktu_tersedia TEXT NOT NULL,     
    jumlah_mhs INT DEFAULT 40,
    jenis_mk VARCHAR(50) DEFAULT 'Teori', 
    semester INT DEFAULT 1,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);