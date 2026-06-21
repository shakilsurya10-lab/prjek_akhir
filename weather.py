import requests


def ambil_cuaca(kota, api_key):
    # URL dasar untuk memanggil data cuaca dari OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric&lang=id"

    try:
        # Mengirim permintaan data ke server
        respons = requests.get(url)
        # Mengubah respons menjadi format JSON/Dictionary Python
        data = respons.json()

        # Jika kode status 200, berarti data berhasil ditemukan
        if data["cod"] == 200:
            nama_kota = data["name"]
            negara = data["sys"]["country"]
            suhu = data["main"]["temp"]
            kelembapan = data["main"]["humidity"]
            deskripsi = data["weather"][0]["description"]
            kecepatan_angin = data["wind"]["speed"]

            print(f"\n--- Informasi Cuaca di {nama_kota}, {negara} ---")
            print(f"Kondisi    : {deskripsi.capitalize()}")
            print(f"Suhu       : {suhu}°C")
            print(f"Kelembapan : {kelembapan}%")
            print(f"Angin      : {kecepatan_angin} m/s")
            print("-" * 40)
        else:
            # Jika kota tidak ditemukan (error 404, dll)
            print(
                f"\n[Error] Kota '{kota}' tidak ditemukan. Silakan periksa kembali ejaannya."
            )

    except requests.exceptions.ConnectionError:
        print("\n[Error] Gagal terhubung ke internet. Periksa koneksi Anda.")
    except Exception as e:
        print(f"\n[Error] Terjadi kesalahan: {e}")


def main():
    # GANTI ini dengan API Key milikmu dari OpenWeatherMap
    API_KEY = "d16609a8a7a2257bde3832ff2b26a373"

    print("=== Aplikasi Cuaca Sederhana ===")

    if API_KEY == "API_KEY_ANDA_DI_SINI":
        print(
            "\n[Peringatan] Kamu belum memasukkan API Key di dalam kode program!"
        )
        return

    while True:
        kota = input("\nMasukkan nama kota (atau ketik 'keluar' untuk berhenti): ")

        if kota.lower() == "keluar":
            print("Terima kasih telah menggunakan aplikasi cuaca!")
            break

        if kota.strip() == "":
            print("Nama kota tidak boleh kosong.")
            continue

        ambil_cuaca(kota, API_KEY)


if __name__ == "__main__":
    main()