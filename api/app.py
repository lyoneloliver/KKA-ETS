from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import saring_kata, pilih_tebakan_berikutnya, muat_kamus, buat_skor_kata
import os 
app = Flask(__name__)
CORS(app)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_path(filename):
    """Mendapatkan path absolut ke file di direktori yang sama."""
    return os.path.join(__location__, filename)


KAMUS_EN = muat_kamus(get_path('kamus-en.txt')) 
SKOR_EN = buat_skor_kata(KAMUS_EN)
print(f"Kamus EN berhasil dimuat, {len(KAMUS_EN) if KAMUS_EN else 0} kata.")

KAMUS_ID = muat_kamus(get_path('kamus-id.txt')) 
SKOR_ID = buat_skor_kata(KAMUS_ID)
print(f"Kamus ID berhasil dimuat, {len(KAMUS_ID) if KAMUS_ID else 0} kata.")


daftar_kata = []
tebakan_saat_ini = None
skor_kata_aktif = {}

@app.route("/start_game", methods=["GET"])
def start_game():
    global daftar_kata, tebakan_saat_ini, skor_kata_aktif
    
    lang = request.args.get('lang', 'en') 

    if lang == 'id' and KAMUS_ID:
        daftar_kata = KAMUS_ID[:]
        skor_kata_aktif = SKOR_ID
        tebakan_saat_ini = pilih_tebakan_berikutnya(daftar_kata, skor_kata_aktif)
        lang_terpilih = "ID"
        
    else:
        
        daftar_kata = KAMUS_EN[:]
        skor_kata_aktif = SKOR_EN
        tebakan_saat_ini = "slate"
        lang_terpilih = "EN"
    
    print(f"--- GAME DIMULAI/DIRESET (Bahasa: {lang_terpilih}) --- Tebakan awal: {tebakan_saat_ini}")
    
    return jsonify({"guess": tebakan_saat_ini})


@app.route("/feedback", methods=["POST"])
def feedback():

    global daftar_kata, tebakan_saat_ini, skor_kata_aktif

    if not tebakan_saat_ini:
        return jsonify({"error": "Permainan belum dimulai."}), 400

    data = request.get_json()
    umpan_balik = data.get("feedback", "").lower()

    if len(umpan_balik) != 5 or not all(c in 'gyb' for c in umpan_balik):
        return jsonify({"error": "Feedback tidak valid."}), 400

    daftar_kata = saring_kata(daftar_kata, tebakan_saat_ini, umpan_balik)
    tebakan_baru = pilih_tebakan_berikutnya(daftar_kata, skor_kata_aktif)

    if not tebakan_baru:
        return jsonify({
            "guess": None,
            "message": "fail_no_match"
        })

    tebakan_saat_ini = tebakan_baru
    return jsonify({
        "guess": tebakan_saat_ini,
        "message": f"{len(daftar_kata)} kata tersisa."
    })

