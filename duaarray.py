def intersection(list1, list2):

    return list(set(list1) & set(list2))


# contoh

a = [1,2,3,4]
b = [3,4,5,6]

print(intersection(a,b))