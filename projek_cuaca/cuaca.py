import requests
from datetime import datetime


def berikan_rekomendasi(deskripsi, suhu):
    """Fungsi untuk memberikan tips tambahan berdasarkan kondisi dan suhu"""
    rekomendasi = []

    # Logika rekomendasi cuaca (hujan/gerimis)
    kata_kunci_hujan = [
        "hujan",
        "gerimis",
        "showering",
        "rain",
        "drizzle",
        "petir",
        "thunderstorm",
    ]
    if any(kata in deskripsi.lower() for kata in kata_kunci_hujan):
        rekomendasi.append("☂️  Siapkan payung atau jas hujan sebelum keluar!")

    # Logika rekomendasi suhu dingin
    if suhu < 22:
        rekomendasi.append("🧥 Suhu cukup dingin, siapkan jaket tebal Anda.")
    elif suhu > 30:
        rekomendasi.append(
            "☀️ Suhu cukup terik, gunakan pakaian yang nyaman dan tetap terhidrasi."
        )

    return rekomendasi
def analisis_aktivitas_outdoor(deskripsi, suhu, kecepatan_angin):
    """FITUR BARU: Menganalisis kelayakan aktivitas luar ruangan (Pendakian & Olahraga)"""
    tips_outdoor = []

    # Standar keselamatan: Hujan lebat/petir atau angin > 10 m/s (sekitar 36 km/jam) sangat berbahaya di gunung
    cuaca_buruk = any(
        kata in deskripsi.lower()
        for kata in ["hujan", "petir", "thunderstorm", "lebat"]
    )

    # 1. Analisis Mode Pendakian (Hiking)
    if cuaca_buruk:
        tips_outdoor.append(
            "❌ [HIKING] SANGAT TIDAK DISARANKAN. Risiko jalur licin, badai, dan hipotermia tinggi."
        )
    elif kecepatan_angin > 8:
        tips_outdoor.append(
            "⚠️ [HIKING] WASPADA! Angin kencang terdeteksi di area terbuka/puncak. Siapkan windbreaker."
        )
    elif suhu < 18:
        tips_outdoor.append(
            "⛰️ [HIKING] Kondisi dingin ideal untuk mendaki, pastikan logistik hangat dan pakaian berlapis siap."
        )
    else:
        tips_outdoor.append(
            "🥾 [HIKING] Cuaca cerah/berawan mendukung untuk pendakian terencana."
        )

    # 2. Analisis Mode Olahraga Harian (Jogging/Sepak Bola/dll)
    if cuaca_buruk:
        tips_outdoor.append(
            "🏠 [OLAHRAGA] Sebaiknya lakukan olahraga dalam ruangan (indoor) hari ini."
        )
    elif 22 <= suhu <= 28 and kecepatan_angin <= 5:
        tips_outdoor.append(
            "🏃 [OLAHRAGA] SANGAT IDEAL! Kondisi udara sejuk dan angin tenang untuk jogging atau olahraga tim."
        )
    elif suhu > 30:
        tips_outdoor.append(
            "🏃 [OLAHRAGA] Cuaca agak terik. Disarankan olahraga di pagi/sore hari dan lipat gandakan minum."
        )
    else:
        tips_outdoor.append(
            "🏃 [OLAHRAGA] Kondisi cukup aman untuk aktivitas luar ruangan biasa."
        )

    return tips_outdoor

def ambil_cuaca_dan_ramalan(kota, api_key):
    # 1. Ambil Cuaca Saat Ini
    url_sekarang = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric&lang=id"

    # 2. Ambil Ramalan Cuaca ke Depan (Menggunakan Forecast API 5 Hari / 3 Jam)
    url_ramalan = f"http://api.openweathermap.org/data/2.5/forecast?q={kota}&appid={api_key}&units=metric&lang=id"

    try:
        # Request Cuaca Saat Ini
        respons_sekarang = requests.get(url_sekarang)
        data_sekarang = respons_sekarang.json()

        if data_sekarang["cod"] == 200:
            nama_kota = data_sekarang["name"]
            negara = data_sekarang["sys"]["country"]
            suhu = data_sekarang["main"]["temp"]
            kelembapan = data_sekarang["main"]["humidity"]
            deskripsi = data_sekarang["weather"][0]["description"]
            kecepatan_angin = data_sekarang["wind"]["speed"]

            # Tampilkan Cuaca Sekarang
            print(f"\n" + "=" * 45)
            print(
                f"--- INFORMASI CUACA SAAT INI: {nama_kota.upper()}, {negara} ---"
            )
            print(f"=" * 45)
            print(f"Kondisi    : {deskripsi.capitalize()}")
            print(f"Suhu       : {suhu}°C")
            print(f"Kelembapan : {kelembapan}%")
            print(f"Angin      : {kecepatan_angin} m/s")

            # Cetak Rekomendasi Pintar
            tips = berikan_rekomendasi(deskripsi, suhu)
            if tips:
                print("\n💡 REKOMENDASI:")
                for tip in tips:
                    print(f"   - {tip}")
            print("-" * 45)

            # Request Ramalan Cuaca Masa Depan
            respons_ramalan = requests.get(url_ramalan)
            data_ramalan = respons_ramalan.json()

            if data_ramalan["cod"] == "200":
                print(f"\n🔮 RAMALAN CUACA BEBERAPA HARI KE DEPAN:")
                print("-" * 45)

                # Mengambil sampel data per hari (interval harian diambil dari jam 12:00 siang)
                hari_terproses = set()
                for prediksi in data_ramalan["list"]:
                    dt_txt = prediksi["dt_txt"]  # Format: "YYYY-MM-DD HH:MM:SS"
                    tanggal = dt_txt.split(" ")[0]
                    waktu = dt_txt.split(" ")[1]

                    if tanggal not in hari_terproses and "12:00:00" in waktu:
                        hari_terproses.add(tanggal)

                        # Konversi tanggal ke format hari Indonesia
                        hari_obj = datetime.strptime(tanggal, "%Y-%m-%d")
                        hari_nama = hari_obj.strftime("%A, %d %b %Y")

                        p_suhu = prediksi["main"]["temp"]
                        p_deskripsi = prediksi["weather"][0]["description"]
                        p_kelembapan = prediksi["main"]["humidity"]

                        print(f"📅 {hari_nama}")
                        print(f"   Kondisi    : {p_deskripsi.capitalize()}")
                        print(f"   Suhu       : {p_suhu}°C")
                        print(f"   Kelembapan : {p_kelembapan}%")

                        # Rekomendasi otomatis untuk ramalan cuaca
                        p_tips = berikan_rekomendasi(p_deskripsi, p_suhu)
                        if p_tips:
                            for tip in p_tips:
                                print(f"   * {tip}")
                        print("-" * 45)

            print("=" * 45)

        else:
            print(
                f"\n[Error] Kota '{kota}' tidak ditemukan. Silakan periksa kembali ejaannya."
            )

    except requests.exceptions.ConnectionError:
        print("\n[Error] Gagal terhubung ke internet. Periksa koneksi Anda.")
    except Exception as e:
        print(f"\n[Error] Terjadi kesalahan saat memproses data: {e}")


def main():
    API_KEY = "d16609a8a7a2257bde3832ff2b26a373"

    print("=== Aplikasi Cuaca Sederhana + Ramalan & Rekomendasi ===")

    # Perbaikan logika pengecekan API Key agar berjalan normal
    if API_KEY.startswith("http") or API_KEY == "API_KEY_ANDA_DI_SINI":
        print(
            "\n[Peringatan] Kamu belum memasukkan API Key yang valid di dalam kode program!"
        )
        return

    while True:
        kota = input(
            "\nMasukkan nama kota (atau ketik 'keluar' untuk berhenti): "
        )

        if kota.lower() == "keluar":
            print("Terima kasih telah menggunakan aplikasi cuaca!")
            break

        if kota.strip() == "":
            print("Nama kota tidak boleh kosong.")
            continue

        ambil_cuaca_dan_ramalan(kota, API_KEY)


if __name__ == "__main__":
    main()