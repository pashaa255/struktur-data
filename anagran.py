def anagram(kata1, kata2):

    return sorted(kata1) == sorted(kata2)


# contoh

print(anagram("listen","silent"))