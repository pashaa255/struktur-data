def first_recurring(kata):

    sudah = set()

    for huruf in kata:

        if huruf in sudah:
            return huruf

        sudah.add(huruf)

    return None


print(first_recurring("programming"))