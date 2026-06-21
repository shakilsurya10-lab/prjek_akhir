from datetime import datetime  # Mengimpor modul untuk waktu real-time
import requests


def ambil_data_cuaca(kota, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric&lang=id"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("❌ Kota tidak ditemukan. Silakan cek kembali ejaannya.")
            return None
        else:
            print(
                f"❌ Gagal mengambil data (Error Code: {response.status_code})"
            )
            return None
    except Exception as e:
        print(f"❌ Terjadi kesalahan jaringan: {e}")
        return None


def dapatkan_rekomendasi(kondisi, suhu):
    if "hujan" in kondisi.lower() or "gerimis" in kondisi.lower():
        pakaian = "Gunakan pakaian hangat/anti air, bawa jas hujan atau payung."
    elif suhu < 22:
        pakaian = (
            "Cuaca cenderung dingin. Gunakan jaket tebal, nyaman, dan hangat."
        )
    elif suhu > 29:
        pakaian = "Cuaca cukup panas. Gunakan pakaian tipis, menyerap keringat, dan bawa kacamata hitam/sunscreen."
    else:
        pakaian = "Cuaca normal. Gunakan pakaian kasual yang nyaman."

    if "hujan" in kondisi.lower() or suhu < 24:
        jenis_kopi = "HOT"
        menu_nescafe = {
            "1. Nescafe Classic Hot": 15000,
            "2. Nescafe Cappuccino Hot": 18000,
            "3. Nescafe Latte Hot": 18000,
        }
    else:
        jenis_kopi = "ICE"
        menu_nescafe = {
            "1. Ice Nescafe Black": 16000,
            "2. Ice Nescafe Latte": 19000,
            "3. Ice Nescafe Caramel Macchiato": 21000,
        }

    return pakaian, jenis_kopi, menu_nescafe


def program_kasir(menu_rekomendasi, nama_kasir):
    print("\n" + "=" * 40)
    print("         SISTEM KASIR NESCAFE         ")
    print("=" * 40)
    print(f"Kasir yang bertugas: {nama_kasir}")
    print("-" * 40)
    print("Daftar Menu Rekomendasi Hari Ini:")

    mapping_menu = {}
    for i, (item, harga) in enumerate(menu_rekomendasi.items(), 1):
        print(f"{i}. {item.split('. ')[1]} - Rp {harga:,}")
        mapping_menu[str(i)] = {"nama": item.split(". ")[1], "harga": harga}

    print("=" * 40)

    pilihan = input("Pilih nomor menu yang ingin dibeli: ").strip()
    if pilihan not in mapping_menu:
        print("❌ Pilihan tidak valid. Transaksi dibatalkan.")
        return

    jumlah = input("Masukkan jumlah pembelian: ")
    if not (Residential_area_digit := jumlah.isdigit()) or int(jumlah) <= 0:
        print("❌ Jumlah harus berupa angka positif. Transaksi dibatalkan.")
        return

    jumlah = int(jumlah)
    item_terpilih = mapping_menu[pilihan]
    total_bayar = item_terpilih["harga"] * jumlah

    print("-" * 40)
    print(f"Detail Order: {item_terpilih['nama']} x {jumlah}")
    print(f"Total Tagihan: Rp {total_bayar:,}")
    print("-" * 40)

    while True:
        try:
            nominal_uang = int(input("Masukkan nominal uang pembayaran: Rp "))
            if nominal_uang < total_bayar:
                print(
                    f"❌ Uang tidak cukup. Kurang sebesar: Rp {total_bayar - nominal_uang:,}"
                )
            else:
                kembalian = nominal_uang - total_bayar

                # --- BAGIAN MENGAMBIL WAKTU TRANSAKSI REAL-TIME ---
                waktu_sekarang = datetime.now()
                # Format: Tanggal-Bulan-Tahun Jam:Menit:Detik
                format_waktu = waktu_sekarang.strftime("%d-%m-%Y %H:%M:%S")

                print("\n" + "=" * 40)
                print("             STRUK PEMBAYARAN             ")
                print("=" * 40)
                print(f"Waktu Transaksi : {format_waktu}")  # Cetak Waktu
                print(f"Kasir           : {nama_kasir}")  # Cetak Kasir
                print("-" * 40)
                print(f"Pesanan         : {item_terpilih['nama']} x {jumlah}")
                print("-" * 40)
                print(f"Total Tagihan   : Rp {total_bayar:,}")
                print(f"Nominal Uang    : Rp {nominal_uang:,}")
                print(f"Kembalian       : Rp {kembalian:,}")
                print("=" * 40)
                print("       Terima kasih telah berbelanja!     ")
                print("=" * 40)
                break
        except ValueError:
            print("❌ Masukkan nominal uang yang valid (angka saja).")


def main():
    API_KEY = "d16609a8a7a2257bde3832ff2b26a373"

    if API_KEY == "MASUKKAN_API_KEY_KAMU_DI_SINI":
        print(
            "⚠️  Silakan ganti variabel 'API_KEY' dengan Kunci API OpenWeatherMap Anda terlebih dahulu!"
        )
        return

    print("=== APLIKASI DETEKSI CUACA & KASIR NESCAFE ===")

    nama_kasir = input("Masukkan nama kasir yang bertugas: ").strip()
    if not nama_kasir:
        nama_kasir = "Kasir Utama"

    kota = input("Masukkan nama kota (contoh: Jakarta, Bandung, Malang): ")

    print("\nSedang mengambil data cuaca...")
    data = ambil_data_cuaca(kota, API_KEY)

    if data:
        nama_kota = data["name"]
        kondisi = data["weather"][0]["description"]
        suhu = data["main"]["temp"]
        kelembapan = data["main"]["humidity"]
        kecepatan_angin = data["wind"]["speed"]

        print("\n" + "=" * 40)
        print(f" KONDISI CUACA SAAT INI DI {nama_kota.upper()} ")
        print("=" * 40)
        print(f"• Kondisi        : {kondisi.capitalize()}")
        print(f"• Suhu           : {suhu} °C")
        print(f"• Kelembapan     : {kelembapan}%")
        print(f"• Kecepatan Angin: {kecepatan_angin} m/s")
        print("-" * 40)

        rekomendasi_pakaian, jenis_kopi, menu_rekomendasi = dapatkan_rekomendasi(
            kondisi, suhu
        )

        print(f"[REKOMENDASI AKTIVITAS & PAKAIAN]")
        print(f"👉 {rekomendasi_pakaian}")
        print(f"\n[REKOMENDASI MENU NESCAFE]")
        print(
            f"👉 Karena cuaca sedang berkondisi '{kondisi}' dengan suhu {suhu}°C,"
        )
        print(f"   menu varian *{jenis_kopi}* sangat cocok untuk menemanimu!")
        print("=" * 40)

        program_kasir(menu_rekomendasi, nama_kasir)


if __name__ == "__main__":
    main()