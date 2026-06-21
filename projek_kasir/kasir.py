import sys
from datetime import datetime


def tampilkan_menu(menu):
    print("\n" + "=" * 45)
    print("         ☕ BOOTH NESCAFE COFFEE BREAK ☕         ")
    print("=" * 45)
    print(f"{'No':<4} | {'Menu Minuman':<25} | {'Harga':<10}")
    print("-" * 45)
    for kode, item in menu.items():
        print(f"{kode:<4} | {item['nama']:<25} | Rp {item['harga']:,}")
    print("-" * 45)


def cetak_struk(keranjang, total, diskon, total_akhir, bayar, kembali, kasir):
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 45)
    print("              NESCAFE COFFEE BOOTH            ")
    print("           Taste the Real Coffee Break        ")
    print("=" * 45)
    print(f"Tanggal : {waktu_sekarang}")
    print(f"Kasir   : {kasir}")
    print("-" * 45)

    for item in keranjang:
        subtotal = item["harga"] * item["jumlah"]
        print(f"{item['nama']}")
        print(f"  {item['jumlah']} x Rp {item['harga']:} Rp {subtotal:,}")

    print("-" * 45)
    print(f"Total Kotor      : Rp {total:,}")
    if diskon > 0:
        print(f"Diskon Promo     : Rp {diskon:,}")
    print(f"Total Bersih     : Rp {total_akhir:,}")
    print(f"Tunai/Bayar      : Rp {bayar:,}")
    print(f"Kembalian        : Rp {kembali:,}")
    print("=" * 45)
    print("       Terima Kasih Atas Kunjungan Anda!      ")
    print("         Sruput Semangatmu Hari Ini!          ")
    print("=" * 45 + "\n")


def main():
    # Menggunakan nama kasir default jika tidak diisi
    nama_kasir = input("Masukkan nama kasir tugas hari ini: ").strip()
    if not nama_kasir:
        nama_kasir = "Staff Nescafe"

    # Data Menu Booth Nescafe
    menu_nescafe = {
        "1": {"nama": "Nescafe Classic Ice", "harga": 12000},
        "2": {"nama": "Nescafe Cappuccino Hot/Ice", "harga": 15000},
        "3": {"nama": "Nescafe Latte Caramel", "harga": 17000},
        "4": {"nama": "Nescafe Moccachino Premium", "harga": 18000},
        "5": {"nama": "Nescafe Americano Bold", "harga": 14000},
        "6": {"nama": "Creamy Hazelnut Latte", "harga": 17000},
    }

    while True:
        keranjang = []
        tampilkan_menu(menu_nescafe)

        # Proses Pemesanan / Input Item
        while True:
            pilihan = (
                input(
                    "Masukkan Nomor Menu (atau ketik 's' untuk Selesai / 'k' untuk Keluar): "
                )
                .strip()
                .lower()
            )

            if pilihan == "k":
                print("\nMenutup aplikasi kasir. Sampai jumpa!")
                sys.exit()

            if pilihan == "s":
                if not keranjang:
                    print("⚠️  Keranjang masih kosong! Silakan pilih menu dulu.")
                    continue
                break

            if pilihan in menu_nescafe:
                try:
                    jumlah = int(
                        input(f"Jumlah untuk {menu_nescafe[pilihan]['nama']}: ")
                    )
                    if jumlah <= 0:
                        print("⚠️  Jumlah pembelian harus lebih dari 0!")
                        continue
                except ValueError:
                    print("⚠️  Input tidak valid! Harap masukkan angka.")
                    continue

                # Masukkan ke keranjang belanja
                keranjang.append(
                    {
                        "nama": menu_nescafe[pilihan]["nama"],
                        "harga": menu_nescafe[pilihan]["harga"],
                        "jumlah": jumlah,
                    }
                )
                print(
                    f"✓ {jumlah} {menu_nescafe[pilihan]['nama']} berhasil ditambahkan."
                )
            else:
                print("⚠️  Nomor menu tidak tersedia, silakan pilih lagi.")

        # Hitung Total Belanjaan
        total_kotor = sum(item["harga"] * item["jumlah"] for item in keranjang)

        # Logika Diskon (Contoh: Diskon Rp 5.000 jika beli di atas Rp 50.000)
        diskon = 0
        if total_kotor >= 50000:
            diskon = 5000
            print(f"\n🎉 Selamat! Mendapatkan diskon promo Nescafe sebesar Rp {diskon:,}")

        total_akhir = total_kotor - diskon
        print(f"\n➡️ Total yang harus dibayar: Rp {total_akhir:,}")

        # Proses Pembayaran
        while True:
            try:
                bayar = int(input("Masukkan nominal uang pembayaran: Rp "))
                if bayar < total_akhir:
                    print(
                        f"⚠️ Uang kurang! Dibutuhkan minimal Rp {total_akhir - bayar:,} lagi."
                    )
                    continue
                break
            except ValueError:
                print("⚠️  Harap masukkan nominal uang berupa angka asli.")

        # Hitung Kembalian & Cetak Struk Resmi
        kembalian = bayar - total_akhir
        cetak_struk(
            keranjang,
            total_kotor,
            diskon,
            total_akhir,
            bayar,
            kembalian,
            nama_kasir,
        )

        # Opsi Transaksi Baru
        ulang = (
            input("Apakah ingin memproses transaksi baru? (y/n): ")
            .strip()
            .lower()
        )
        if ulang != "y":
            print("\nTerima kasih! Program kasir Nescafe dimatikan.")
            break


if __name__ == "__main__":
    main()