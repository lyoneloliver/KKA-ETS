
from collections import Counter, defaultdict


def muat_kamus(nama_file):
    try:
        with open(nama_file, 'r', encoding='utf-8') as file:
            daftar_kata = [baris.strip().lower() for baris in file]
        hasil = [kata for kata in daftar_kata if len(kata) == 5]
        if not hasil:
            print(f"Peringatan: Tidak ada kata 5 huruf di {nama_file}")
        return hasil
    except FileNotFoundError:
        print(f"ERROR: File '{nama_file}' tidak ditemukan.")
        return []
    except Exception as e:
        print(f"Error saat baca file {nama_file}: {e}")
        return []



def hitung_frekuensi_huruf(daftar_kata):
    freq = Counter()
    for kata in daftar_kata:
        freq.update(kata)
    return freq

def buat_skor_kata(daftar_kata):
    if not daftar_kata:
        return {}
    freq = hitung_frekuensi_huruf(daftar_kata)
    skor = {}
    for kata in daftar_kata:
        huruf_unik = set(kata)
        nilai = sum(freq[h] for h in huruf_unik)
        if len(huruf_unik) == 5:
            nilai *= 1.2
        skor[kata] = int(nilai)
    return skor



class WordleCSP:
    def __init__(self, kamus):
        self.kamus_awal = kamus
        self.kandidat = kamus[:]   
        self.constraint_hijau = {} 
        self.constraint_kuning = defaultdict(set) 
        self.constraint_ada = Counter()  
        self.constraint_tidak_ada = set()  

    def tambah_feedback(self, tebakan, feedback):
        """
        Update constraint CSP berdasarkan hasil feedback.
        g = green, y = yellow, b = black/gray
        """
        for i, (huruf, fb) in enumerate(zip(tebakan, feedback)):
            if fb == 'g':  
                self.constraint_hijau[i] = huruf
                self.constraint_ada[huruf] += 1
            elif fb == 'y':  
                self.constraint_kuning[i].add(huruf)
                self.constraint_ada[huruf] += 1
            elif fb == 'b':  
                if huruf not in self.constraint_ada:
                    self.constraint_tidak_ada.add(huruf)

    def konsisten(self, kata):
        """Periksa apakah kata memenuhi semua constraint CSP."""
        
        for i, huruf in self.constraint_hijau.items():
            if kata[i] != huruf:
                return False

        
        for pos, huruf_set in self.constraint_kuning.items():
            for h in huruf_set:
                if kata[pos] == h or h not in kata:
                    return False

        
        for huruf, jumlah_min in self.constraint_ada.items():
            if kata.count(huruf) < jumlah_min:
                return False

        
        for huruf in self.constraint_tidak_ada:
            if huruf in kata:
                return False

        return True

    def saring_domain(self):
        """Filter domain sesuai constraint aktif."""
        self.kandidat = [k for k in self.kandidat if self.konsisten(k)]

    def ambil_tebakan(self, skor_dict):
        """Pilih tebakan dengan skor tertinggi dari domain yang valid."""
        if not self.kandidat:
            return None
        terbaik = sorted(self.kandidat, key=lambda k: skor_dict.get(k, 0), reverse=True)
        return terbaik[0]



def saring_kata(daftar_kata, tebakan_terakhir, feedback):
    
    csp = WordleCSP(daftar_kata)
    csp.tambah_feedback(tebakan_terakhir, feedback)
    csp.saring_domain()
    return csp.kandidat


def pilih_tebakan_berikutnya(daftar_kata, skor_kata_kamus):
    if not daftar_kata:
        return None
    kata_terurut = sorted(
        daftar_kata,
        key=lambda k: skor_kata_kamus.get(k, 0),
        reverse=True
    )
    return kata_terurut[0]
