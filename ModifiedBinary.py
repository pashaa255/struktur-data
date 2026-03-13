"""
Praktikum — Chapter 5: Data Structures & Algorithms
Solusi lengkap untuk Soal 1–5
"""

import time
import random

# ─────────────────────────────────────────────
# SOAL 1 — Modified Binary Search
# ─────────────────────────────────────────────

def countOccurrences(sortedList, target):
    """
    Menghitung berapa kali target muncul dalam sorted list.
    Kompleksitas: O(log n) menggunakan dua binary search.
    """
    def find_left(arr, t):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t:
                result = mid
                hi = mid - 1      # terus cari ke kiri
            elif arr[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    def find_right(arr, t):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t:
                result = mid
                lo = mid + 1      # terus cari ke kanan
            elif arr[mid] < t:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    left  = find_left(sortedList, target)
    if left == -1:
        return 0
    right = find_right(sortedList, target)
    return right - left + 1


# ─────────────────────────────────────────────
# SOAL 2 — Bubble Sort dengan Analisis Langkah
# ─────────────────────────────────────────────

def bubbleSort(arr):
    """
    Modified bubble sort yang mengembalikan:
    (sorted_list, total_comparisons, total_swaps, passes_used)
    Dilengkapi early termination dan mencetak state per pass.
    """
    a = arr[:]
    n = len(a)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    for pass_num in range(1, n):
        swapped = False
        for i in range(n - pass_num):
            total_comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                total_swaps += 1
                swapped = True
        passes_used += 1
        print(f"  Pass {pass_num}: {a}")
        if not swapped:      # early termination
            break

    return (a, total_comparisons, total_swaps, passes_used)


# ─────────────────────────────────────────────
# SOAL 3 — Hybrid Sort
# ─────────────────────────────────────────────

def _insertion_sort_counted(arr, lo, hi):
    """Insertion sort pada arr[lo..hi], kembalikan (comparisons, swaps)."""
    comps = swaps = 0
    for i in range(lo + 1, hi + 1):
        key = arr[i]
        j = i - 1
        while j >= lo and arr[j] > key:
            comps += 1
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        if j >= lo:
            comps += 1          # perbandingan yang gagal
        arr[j + 1] = key
    return comps, swaps


def _selection_sort_counted(arr, lo, hi):
    """Selection sort pada arr[lo..hi], kembalikan (comparisons, swaps)."""
    comps = swaps = 0
    for i in range(lo, hi + 1):
        min_idx = i
        for j in range(i + 1, hi + 1):
            comps += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return comps, swaps


def hybridSort(theSeq, threshold=10):
    """
    Hybrid sort: insertion sort jika panjang sub-array ≤ threshold,
    selection sort jika lebih besar.
    Kembalikan (sorted_list, total_comparisons, total_swaps).
    """
    arr = theSeq[:]
    total_comps = total_swaps = 0

    def _sort(lo, hi):
        nonlocal total_comps, total_swaps
        if lo >= hi:
            return
        size = hi - lo + 1
        if size <= threshold:
            c, s = _insertion_sort_counted(arr, lo, hi)
        else:
            # Gunakan selection sort per blok threshold, lalu merge
            # Pendekatan sederhana: selection sort seluruh rentang
            c, s = _selection_sort_counted(arr, lo, hi)
        total_comps += c
        total_swaps += s

    _sort(0, len(arr) - 1)
    return arr, total_comps, total_swaps


def _pure_insertion_sort(theSeq):
    arr = theSeq[:]
    comps = swaps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comps += 1
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        if j >= 0:
            comps += 1
        arr[j + 1] = key
    return arr, comps, swaps


def _pure_selection_sort(theSeq):
    arr = theSeq[:]
    comps = swaps = 0
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            comps += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, comps, swaps


# ─────────────────────────────────────────────
# SOAL 4 — Merge Tiga Sorted Lists
# ─────────────────────────────────────────────

def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan tiga sorted list menjadi satu sorted list
    dalam O(n) menggunakan tiga pointer (single pass).
    """
    result = []
    i = j = k = 0
    a, b, c = len(listA), len(listB), len(listC)

    while i < a or j < b or k < c:
        # Ambil nilai saat ini (inf jika pointer sudah habis)
        va = listA[i] if i < a else float('inf')
        vb = listB[j] if j < b else float('inf')
        vc = listC[k] if k < c else float('inf')

        if va <= vb and va <= vc:
            result.append(va); i += 1
        elif vb <= va and vb <= vc:
            result.append(vb); j += 1
        else:
            result.append(vc); k += 1

    return result


# ─────────────────────────────────────────────
# SOAL 5 — Inversions Counter
# ─────────────────────────────────────────────

def countInversionsNaive(arr):
    """Brute force O(n²): hitung semua pasangan (i,j) di mana i<j dan arr[i]>arr[j]."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def countInversionsSmart(arr):
    """
    Modifikasi merge sort O(n log n):
    Saat merge, setiap kali elemen dari kanan diambil lebih dulu,
    semua elemen kiri yang tersisa adalah inversions.
    """
    def merge_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left,  lc = merge_count(a[:mid])
        right, rc = merge_count(a[mid:])
        merged = []
        inversions = lc + rc
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                # left[i..] semua lebih besar dari right[j]
                inversions += len(left) - i
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    _, count = merge_count(arr)
    return count


# ══════════════════════════════════════════════
# DEMO & TESTING
# ══════════════════════════════════════════════

def separator(title):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print('═'*60)


# ── Soal 1 ──────────────────────────────────
separator("SOAL 1 — Modified Binary Search")

arr1 = [1, 2, 4, 4, 4, 4, 7, 9, 12]
print(f"Array: {arr1}")
print(f"countOccurrences(arr, 4) → {countOccurrences(arr1, 4)}  (expected: 4)")
print(f"countOccurrences(arr, 5) → {countOccurrences(arr1, 5)}  (expected: 0)")
print(f"countOccurrences(arr, 1) → {countOccurrences(arr1, 1)}  (expected: 1)")
print(f"countOccurrences(arr, 12)→ {countOccurrences(arr1, 12)} (expected: 1)")


# ── Soal 2 ──────────────────────────────────
separator("SOAL 2 — Bubble Sort dengan Analisis Langkah")

for test_arr in [[5, 1, 4, 2, 8], [1, 2, 3, 4, 5]]:
    print(f"\nInput: {test_arr}")
    sorted_arr, comps, swaps, passes = bubbleSort(test_arr)
    print(f"  → Sorted     : {sorted_arr}")
    print(f"  → Comparisons: {comps}")
    print(f"  → Swaps      : {swaps}")
    print(f"  → Passes     : {passes}")

print("""
Penjelasan perbedaan jumlah pass:
  [5,1,4,2,8]: tidak terurut → banyak swap → butuh lebih banyak pass.
  [1,2,3,4,5]: sudah terurut → pass pertama tidak ada swap →
               early termination langsung berhenti di pass ke-1.
""")


# ── Soal 3 ──────────────────────────────────
separator("SOAL 3 — Hybrid Sort")

print(f"\n{'Ukuran':>8} | {'Hybrid (C+S)':>14} | {'Insertion (C+S)':>16} | {'Selection (C+S)':>16}")
print("-" * 62)

for size in [50, 100, 500]:
    data = [random.randint(1, 1000) for _ in range(size)]
    _, hc, hs = hybridSort(data)
    _, ic, is_ = _pure_insertion_sort(data)
    _, sc, ss = _pure_selection_sort(data)
    print(f"{size:>8} | {hc+hs:>14} | {ic+is_:>16} | {sc+ss:>16}")

print("\nCatatan: C = comparisons, S = swaps")


# ── Soal 4 ──────────────────────────────────
separator("SOAL 4 — Merge Tiga Sorted Lists")

listA = [1, 5, 9]
listB = [2, 6, 10]
listC = [3, 4, 7]
result = mergeThreeSortedLists(listA, listB, listC)
print(f"mergeThreeSortedLists({listA}, {listB}, {listC})")
print(f"→ {result}")
print(f"  (expected: [1, 2, 3, 4, 5, 6, 7, 9, 10])")

# Test tambahan
listX = [1, 4, 7]
listY = [2, 5, 8]
listZ = [3, 6, 9]
print(f"\nmergeThreeSortedLists({listX}, {listY}, {listZ})")
print(f"→ {mergeThreeSortedLists(listX, listY, listZ)}")


# ── Soal 5 ──────────────────────────────────
separator("SOAL 5 — Inversions Counter")

# Verifikasi kesamaan hasil
test_cases = [
    [2, 4, 1, 3, 5],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [3, 1, 2],
]
print("\nVerifikasi Naive == Smart:")
for tc in test_cases:
    naive  = countInversionsNaive(tc)
    smart  = countInversionsSmart(tc)
    match  = "✓" if naive == smart else "✗"
    print(f"  {tc}  →  Naive={naive}, Smart={smart}  {match}")

# Benchmark
print(f"\n{'Ukuran':>8} | {'Naive (ms)':>12} | {'Smart (ms)':>12}")
print("-" * 38)

for size in [1000, 5000, 10000]:
    data = [random.randint(1, size * 10) for _ in range(size)]

    t0 = time.perf_counter()
    countInversionsNaive(data)
    t_naive = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    countInversionsSmart(data)
    t_smart = (time.perf_counter() - t0) * 1000

    print(f"{size:>8} | {t_naive:>11.2f}ms | {t_smart:>11.2f}ms")

print("""""
Mengapa merge sort lebih cepat?
  • Naive O(n²) : memeriksa SEMUA pasangan (i,j) → untuk n=10000
    itu ~50 juta iterasi.
  • Smart O(n log n): saat merge, kita bisa menghitung inversions
    untuk seluruh sisa subarray kiri sekaligus (tanpa loop per elemen),
    sehingga total operasi jauh lebih sedikit (~130 ribu untuk n=10000).
  Rasio: n² / (n log n) = n / log n → makin besar n, makin besar
  keunggulan merge sort.
""") 

print("""\nSemua soal telah selesai.
      Terima kasih sudah mengikuti praktikum ini!""")