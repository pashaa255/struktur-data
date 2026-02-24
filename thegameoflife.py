import time
import os

# ukuran grid
BARIS = 10
KOLOM = 10

# membuat grid kosong
def buat_grid():
    grid = []
    for i in range(BARIS):
        baris = []
        for j in range(KOLOM):
            baris.append(0)
        grid.append(baris)
    return grid

# menampilkan grid
def tampilkan(grid):
    os.system("cls")  # untuk Windows
    for i in range(BARIS):
        for j in range(KOLOM):
            if grid[i][j] == 1:
                print("■", end=" ")
            else:
                print(".", end=" ")
        print()

# menghitung tetangga hidup
def hitung_tetangga(grid, x, y):
    jumlah = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx = x + i
            ny = y + j
            if 0 <= nx < BARIS and 0 <= ny < KOLOM:
                jumlah += grid[nx][ny]
    return jumlah

# membuat generasi baru
def generasi_baru(grid):
    baru = buat_grid()
    for i in range(BARIS):
        for j in range(KOLOM):
            tetangga = hitung_tetangga(grid, i, j)

            if grid[i][j] == 1:
                if tetangga == 2 or tetangga == 3:
                    baru[i][j] = 1
                else:
                    baru[i][j] = 0
            else:
                if tetangga == 3:
                    baru[i][j] = 1
    return baru

# program utama
grid = buat_grid()

# contoh pola awal
grid[4][4] = 1
grid[4][5] = 1
grid[4][6] = 1

# jalankan simulasi
for i in range(20):
    tampilkan(grid)
    grid = generasi_baru(grid)
    time.sleep(0.5)