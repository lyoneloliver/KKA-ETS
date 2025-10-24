# Wordle Solver

Ini adalah aplikasi *solver* untuk game Wordle yang menggunakan *backend* Python dengan Flask dan *frontend* berbasis web (HTML, CSS, JavaScript). Aplikasi ini secara cerdas akan memberikan tebakan kata, dan Anda hanya perlu memberikan umpan balik berupa warna (hijau, kuning, abu-abu) dari hasil tebakan di game Wordle yang sebenarnya.

Solver ini mendukung dua bahasa: **Inggris** dan **Indonesia**.

##  Fitur Utama

  * **Tebakan Cerdas**: Menggunakan pendekatan *Constraint Satisfaction Problem* (CSP) untuk menyaring daftar kata yang mungkin.
  * **Pemilihan Kata Terbaik**: Memilih kata tebakan berikutnya berdasarkan frekuensi huruf untuk memaksimalkan informasi yang didapat.
  * **Dukungan Multi-bahasa**: Dapat beralih antara kamus bahasa Inggris dan Indonesia.
  * **Antarmuka Web Interaktif**: Frontend sederhana untuk memasukkan umpan balik warna dengan mudah.
  * **Arsitektur Client-Server**: Logika solver berjalan di server Python (Flask), sementara antarmuka pengguna berjalan di browser.

## 🛠️ Teknologi yang Digunakan

  * **Backend**: Python, Flask, Flask-CORS
  * **Frontend**: HTML, CSS, JavaScript
  * **Konsep Inti**: Constraint Satisfaction Problem (CSP), Heuristik, Analisis Frekuensi

## Struktur Folder Proyek

Agar proyek ini berjalan dengan benar, pastikan struktur file Anda terlihat seperti ini:

```
/wordle-solver
|-- app.py             # Server Flask (backend utama)
|-- solver.py          # Logika inti Wordle solver (CSP)
|-- wordle.html        # Halaman antarmuka (frontend)
|-- wordle.css         # Styling untuk halaman
|-- wordle.js          # Logika interaksi di frontend
|-- kamus-en.txt       # Daftar kata 5 huruf bahasa Inggris
|-- kamus-id.txt       # Daftar kata 5 huruf bahasa Indonesia
|-- requirements.txt   # Daftar dependensi Python
```

-----

## Instalasi dan Cara Menjalankan

Ikuti langkah-langkah ini untuk menjalankan proyek di komputer Anda.

### **Prasyarat**

  * **Python 3.x** terinstal di sistem Anda.
  * **Git** untuk melakukan clone repositori.

### **Langkah 1: Clone Repositori**

Buka terminal atau command prompt dan jalankan perintah berikut:

```sh
git clone [URL-repositori-Anda]
cd [nama-folder-repositori]
```

### **Langkah 2: Siapkan Kamus Kata**

Proyek ini memerlukan dua file teks sebagai sumber kamus kata:

1.  Buat file bernama `kamus-en.txt`.
2.  Buat file bernama `kamus-id.txt`.

Isi kedua file tersebut dengan daftar kata 5 huruf (satu kata per baris) sesuai bahasanya. Anda bisa mencari daftar kata di internet.

### **Langkah 3: Siapkan Lingkungan Python & Instal Dependensi**

Sangat disarankan untuk menggunakan *virtual environment*.

```sh
# Buat virtual environment 
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate

# MacOS/Linux:
source venv/bin/activate
```

Selanjutnya, buat file `requirements.txt` dan isi dengan teks berikut:

```txt
Flask
Flask-Cors
```

Lalu, instal semua dependensi dengan perintah:

```sh
pip install -r requirements.txt
```

### **Langkah 4: Jalankan Proyek**

Proyek ini terdiri dari dua bagian yang perlu dijalankan secara terpisah.

**1. Jalankan Server Backend**
Di terminal Anda (dengan virtual environment yang masih aktif), jalankan server Flask:

```sh
python app.py
```

Anda akan melihat pesan bahwa server berjalan di `http://127.0.0.1:5000`. **Biarkan terminal ini tetap terbuka.**

**2. Buka Antarmuka Frontend**
Buka file `wordle.html` langsung di browser web Anda (misalnya dengan klik dua kali pada file tersebut).

-----

## Cara Menggunakan Aplikasi

1.  Buka `wordle.html` di browser.
2.  Pilih bahasa (EN/ID) yang ingin digunakan. Aplikasi akan memberikan tebakan awal (misal: "slate").
3.  Masukkan kata tebakan tersebut ke dalam game Wordle yang asli.
4.  Setelah mendapatkan hasilnya di game Wordle, kembali ke aplikasi solver. Klik pada setiap huruf di baris tebakan untuk mengubah warnanya sesuai hasil (Hijau, Kuning, Abu-abu).
5.  Setelah semua warna sesuai, klik tombol **"Kirim Feedback"**.
6.  Solver akan memproses umpan balik dan memberikan tebakan terbaik berikutnya.
7.  Ulangi langkah 3-6 sampai kata ditemukan.
8.  Gunakan tombol **"Mulai Ulang"** untuk mereset solver dan memulai permainan baru.