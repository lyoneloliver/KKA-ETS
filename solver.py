# solver.py

import random
from collections import Counter

def muat_kamus(nama_file):
    """Membaca file kamus dan mengembalikan list berisi kata 5 huruf."""
    try:
        with open(nama_file, 'r', encoding='utf-8') as file:
            daftar_kata = [baris.strip().lower() for baris in file]
        hasil = [kata for kata in daftar_kata if len(kata) == 5]
        if not hasil:
            print(f"Peringatan: Tidak ada kata 5 huruf yang ditemukan di {nama_file}")
        return hasil
    except FileNotFoundError:
        print(f"ERROR: File kamus '{nama_file}' tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Error saat membaca file {nama_file}: {e}")
        return None

# --- Bagian Penskuran Kata ---

def hitung_frekuensi_huruf(daftar_kata):
    """Menghitung frekuensi total setiap huruf di seluruh kamus."""
    counts = Counter()
    for kata in daftar_kata:
        counts.update(kata)
    return counts

def buat_skor_kata(daftar_kata):
    """
    Membuat dictionary {kata: skor} untuk setiap kata di kamus.
    """
    if not daftar_kata:
        return {}
        
    freq = hitung_frekuensi_huruf(daftar_kata)
    skor_kata = {}

    for kata in daftar_kata:
        skor = 0
        huruf_unik = set(kata)
        for huruf in huruf_unik:
            skor += freq.get(huruf, 0) 
        if len(huruf_unik) == 5:
            skor = int(skor * 1.2)
        skor_kata[kata] = skor
    return skor_kata

# --- Fungsi Penyaringan (Filter) ---

def saring_kata(daftar_kata, tebakan_terakhir, umpan_balik):
    """
    Fungsi inti yang menyaring daftar kata (penanganan huruf ganda).
    """
    if not daftar_kata:
        return []

    huruf_hijau = {i: tebakan_terakhir[i] for i, char in enumerate(umpan_balik) if char == 'g'}
    huruf_kuning = {i: tebakan_terakhir[i] for i, char in enumerate(umpan_balik) if char == 'y'}
    huruf_abu = {tebakan_terakhir[i] for i, char in enumerate(umpan_balik) if char == 'b'}
    jumlah_huruf_min = Counter(list(huruf_hijau.values()) + list(huruf_kuning.values()))
    
    kata_yang_memenuhi = []
    for kata in daftar_kata:
        valid = True
        
        for pos, huruf in huruf_hijau.items():
            if kata[pos] != huruf: valid = False; break
        if not valid: continue

        for pos, huruf in huruf_kuning.items():
            if kata[pos] == huruf or huruf not in kata: valid = False; break
        if not valid: continue
            
        for huruf in huruf_abu:
            if huruf not in jumlah_huruf_min and huruf in kata: valid = False; break
        if not valid: continue
            
        for huruf, jumlah in jumlah_huruf_min.items():
            if kata.count(huruf) < jumlah: valid = False; break
        if not valid: continue

        kata_yang_memenuhi.append(kata)
        
    return kata_yang_memenuhi

# --- Fungsi Pemilihan (Sortir) ---

def pilih_tebakan_berikutnya(daftar_kata, skor_kata_kamus):
    if not daftar_kata:
        return None
    
    kata_terurut = sorted(
        daftar_kata, 
        key=lambda kata: skor_kata_kamus.get(kata, 0),
        reverse=True
    )
    
    return kata_terurut[0]
