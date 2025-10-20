# server_solver.py

from flask import Flask, request, jsonify
from flask_cors import CORS
# Impor globals dan fungsi dari solver.py
from solver import saring_kata, pilih_tebakan_berikutnya, KAMUS_LENGKAP

# --- Inisialisasi Aplikasi Flask ---
app = Flask(__name__)
CORS(app)

# --- State Global ---
if not KAMUS_LENGKAP:
    print("ERROR: KAMUS_LENGKAP dari solver.py kosong. Pastikan kamus-id.txt ada.")
    
# Variabel state game, akan di-reset oleh /start_game
daftar_kata = []
tebakan_saat_ini = None


# --- API Endpoint ---

@app.route("/start_game", methods=["GET"])
def start_game():
    """
    Me-reset state server DAN mengirim tebakan awal.
    """
    global daftar_kata, tebakan_saat_ini
    
    # 1. Reset state
    if KAMUS_LENGKAP:
        daftar_kata = KAMUS_LENGKAP[:] # Salin kamus lengkap
    else:
        daftar_kata = []
    
    # 2. === PERUBAHAN DI SINI ===
    # Mengganti tebakan strategis dengan 'lates'
    # tebakan_saat_ini = pilih_tebakan_berikutnya(daftar_kata) # <-- Versi lama
    tebakan_saat_ini = "slate" # <-- Versi baru
    
    print(f"--- GAME DIMULAI/DIRESET --- Tebakan awal: {tebakan_saat_ini}")
    
    # 3. Kirim tebakan
    return jsonify({"guess": tebakan_saat_ini})


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Endpoint untuk menerima feedback warna dari frontend,
    memprosesnya, dan mengirimkan tebakan berikutnya.
    """
    global daftar_kata, tebakan_saat_ini

    if not tebakan_saat_ini:
        return jsonify({"error": "Permainan belum dimulai. Panggil /start_game dulu."}), 400

    data = request.get_json()
    umpan_balik = data.get("feedback", "").lower()

    if len(umpan_balik) != 5 or not all(c in 'gyb' for c in umpan_balik):
        return jsonify({"error": "Feedback tidak valid. Harus 5 karakter g/y/b."}), 400

    # Saring daftar kata berdasarkan tebakan terakhir dan umpan balik
    daftar_kata = saring_kata(daftar_kata, tebakan_saat_ini, umpan_balik)
    
    # Pilih tebakan baru yang TERBAIK dari sisa kata
    tebakan_baru = pilih_tebakan_berikutnya(daftar_kata)

    if not tebakan_baru:
        return jsonify({
            "guess": None,
            "message": "Tidak ada kata yang cocok di kamus. Solver menyerah."
        })

    # Perbarui tebakan saat ini untuk siklus berikutnya
    tebakan_saat_ini = tebakan_baru
    return jsonify({
        "guess": tebakan_saat_ini,
        "message": f"{len(daftar_kata)} kata tersisa."
    })

# --- Menjalankan Server ---
if __name__ == "__main__":
    print(f"Kamus berhasil dimuat, {len(KAMUS_LENGKAP) if KAMUS_LENGKAP else 0} kata.")
    print("-> Server solver berjalan di http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)