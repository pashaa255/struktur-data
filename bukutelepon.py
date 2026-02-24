kontak = {}

while True:

    print("\n1. Tambah")
    print("2. Cari")
    print("3. Tampilkan")
    print("4. Keluar")

    pilih = input("Pilih : ")

    if pilih == "1":

        nama = input("Nama : ")
        nomor = input("Nomor : ")

        kontak[nama] = nomor

    elif pilih == "2":

        nama = input("Cari nama : ")

        print(kontak.get(nama,"Tidak ada"))

    elif pilih == "3":

        for nama, nomor in kontak.items():

            print(nama, nomor)

    elif pilih == "4":

        break