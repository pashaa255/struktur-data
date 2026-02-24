def deduplikasi(data):
    sudah = set()
    hasil = []

    for item in data:
        if item not in sudah:
            hasil.append(item)
            sudah.add(item)

    return hasil


# contoh
data = [1,2,2,3,1,4,3]
print(deduplikasi(data))