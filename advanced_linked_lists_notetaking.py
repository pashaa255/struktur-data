"""
==========================================
TUGAS: Advanced Linked Lists
Slide 39 - Aplikasi Note-Taking
==========================================

Rancang struktur data untuk aplikasi note-taking yang mendukung:
1. Multiple tags per note (multi-linked by tag)
2. Chronological dan alphabetical views (doubly linked sorted)
3. Sync status tracking (circular buffer for recent changes)

Nama   : [Nama Kamu]
NIM    : [NIM Kamu]
Matkul : Struktur Data Lanjut
"""

from datetime import datetime


# ============================================================
# BAGIAN 1: NODE DEFINITIONS
# ============================================================

class NoteNode:
    """
    Node utama untuk setiap catatan (note).
    Menggunakan Multi-Linked List:
      - next_chron / prev_chron : doubly linked by chronological order
      - next_alpha / prev_alpha : doubly linked by alphabetical order
    Setiap node juga memiliki daftar tag yang terhubung.
    """
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.tags: list[str] = []          # daftar tag pada note ini

        # Doubly linked - chronological chain
        self.next_chron = None
        self.prev_chron = None

        # Doubly linked - alphabetical chain
        self.next_alpha = None
        self.prev_alpha = None

    def __repr__(self):
        return (f"Note(title='{self.title}', "
                f"tags={self.tags}, "
                f"created={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})")


class TagNode:
    """
    Node untuk Tag Index.
    Setiap tag memiliki linked list sendiri yang menunjuk ke semua NoteNode
    yang memiliki tag tersebut (partial chain / secondary index).
    """
    def __init__(self, tag_name: str, note_ref: NoteNode):
        self.tag_name = tag_name
        self.note_ref = note_ref   # referensi ke NoteNode
        self.next = None           # next TagNode dengan tag yang sama


class SyncEntry:
    """
    Entry untuk Circular Buffer sinkronisasi.
    Menyimpan info perubahan terakhir (Recent Changes).
    """
    def __init__(self, action: str, note_title: str):
        self.action = action           # 'ADD', 'DELETE', 'TAG_ADD', dll.
        self.note_title = note_title
        self.timestamp = datetime.now()
        self.next = None               # circular link

    def __repr__(self):
        return (f"[{self.timestamp.strftime('%H:%M:%S')}] "
                f"{self.action}: '{self.note_title}'")


# ============================================================
# BAGIAN 2: CIRCULAR BUFFER (Sync Status Tracking)
# ============================================================

class CircularSyncBuffer:
    """
    Circular Buffer untuk melacak N perubahan terakhir.
    Menggunakan Circular Linked List:
      - listRef menunjuk ke node TERAKHIR yang dimasukkan
      - listRef.next = node PERTAMA (oldest entry)
    Kapasitas tetap: jika penuh, entry terlama diganti.
    """

    def __init__(self, capacity: int = 5):
        self.capacity = capacity
        self.size = 0
        self.listRef = None    # menunjuk ke node TERAKHIR (newest)

    def add(self, action: str, note_title: str):
        """Tambah entry baru ke circular buffer."""
        new_entry = SyncEntry(action, note_title)

        if self.listRef is None:
            # Buffer kosong
            new_entry.next = new_entry
            self.listRef = new_entry
            self.size = 1
        elif self.size < self.capacity:
            # Buffer belum penuh, tambah node baru
            new_entry.next = self.listRef.next   # new -> oldest
            self.listRef.next = new_entry        # prev_last -> new
            self.listRef = new_entry             # listRef = new (newest)
            self.size += 1
        else:
            # Buffer penuh: timpa entry terlama
            # listRef.next = oldest; kita timpa oldest
            oldest = self.listRef.next
            new_entry.next = oldest.next         # new -> second-oldest
            self.listRef.next = new_entry        # prev_last -> new
            self.listRef = new_entry             # listRef = new

    def get_all(self) -> list:
        """
        Kembalikan semua entry dari TERBARU ke TERLAMA.
        Traversal: mulai dari listRef (newest), mundur via circular.
        """
        if self.listRef is None:
            return []

        results = []
        curNode = self.listRef
        done = False
        while not done:
            results.append(curNode)
            curNode = curNode.next
            done = (curNode is self.listRef)

        # Urutan saat ini: oldest -> newest (karena kita mulai dari newest.next)
        # Balik agar newest tampil pertama
        results.reverse()
        return results

    def display(self):
        """Tampilkan isi circular buffer."""
        entries = self.get_all()
        print(f"\n=== Sync History (last {self.capacity} changes) ===")
        if not entries:
            print("  (kosong)")
        for i, e in enumerate(entries):
            print(f"  {i+1}. {e}")


# ============================================================
# BAGIAN 3: NOTE-TAKING APP
# ============================================================

class NoteTakingApp:
    """
    Aplikasi Note-Taking dengan Advanced Linked Lists.

    Struktur data yang digunakan:
    - Doubly Linked List (chronological): head_chron / tail_chron
    - Doubly Linked List (alphabetical): head_alpha / tail_alpha
    - Multi-Linked by Tag: tag_index dict -> TagNode linked list
    - Circular Buffer: sync_buffer untuk recent changes
    """

    def __init__(self, sync_capacity: int = 5):
        # Chain 1: Doubly Linked - Chronological (insert order = time order)
        self.head_chron = None
        self.tail_chron = None

        # Chain 2: Doubly Linked - Alphabetical (sorted by title)
        self.head_alpha = None
        self.tail_alpha = None

        # Tag Index: tag_name -> kepala TagNode linked list
        self.tag_index: dict[str, TagNode] = {}

        # Circular Buffer untuk sync
        self.sync_buffer = CircularSyncBuffer(capacity=sync_capacity)

        self.count = 0

    # ----------------------------------------------------------
    # INSERT NOTE
    # ----------------------------------------------------------
    def add_note(self, title: str, content: str, tags: list[str] = None):
        """
        Tambahkan note baru:
        - Append ke ujung chronological chain (newest last)
        - Insert sorted ke alphabetical chain
        - Daftarkan ke setiap tag chain
        - Catat ke sync buffer
        """
        new_node = NoteNode(title, content)
        if tags:
            new_node.tags = list(tags)

        # 1) Chronological: tambah ke TAIL (paling baru = paling belakang)
        self._insert_chron(new_node)

        # 2) Alphabetical: insert sorted by title (ascending)
        self._insert_alpha_sorted(new_node)

        # 3) Tag index: daftarkan ke setiap tag
        for tag in new_node.tags:
            self._register_tag(tag, new_node)

        # 4) Sync buffer
        self.sync_buffer.add("ADD", title)
        self.count += 1
        print(f"[+] Note '{title}' berhasil ditambahkan.")

    def _insert_chron(self, new_node: NoteNode):
        """Append ke tail chronological chain."""
        if self.head_chron is None:
            self.head_chron = self.tail_chron = new_node
        else:
            new_node.prev_chron = self.tail_chron
            self.tail_chron.next_chron = new_node
            self.tail_chron = new_node

    def _insert_alpha_sorted(self, new_node: NoteNode):
        """Insert sorted ascending by title ke alphabetical chain."""
        title = new_node.title.lower()

        # Case: kosong
        if self.head_alpha is None:
            self.head_alpha = self.tail_alpha = new_node
            return

        # Case: lebih kecil dari head
        if title <= self.head_alpha.title.lower():
            new_node.next_alpha = self.head_alpha
            self.head_alpha.prev_alpha = new_node
            self.head_alpha = new_node
            return

        # Case: lebih besar dari tail
        if title >= self.tail_alpha.title.lower():
            new_node.prev_alpha = self.tail_alpha
            self.tail_alpha.next_alpha = new_node
            self.tail_alpha = new_node
            return

        # Case: tengah - cari posisi
        cur = self.head_alpha
        while cur is not None and cur.title.lower() < title:
            cur = cur.next_alpha

        # Insert sebelum cur
        prev_node = cur.prev_alpha
        new_node.next_alpha = cur
        new_node.prev_alpha = prev_node
        prev_node.next_alpha = new_node
        cur.prev_alpha = new_node

    def _register_tag(self, tag: str, note_node: NoteNode):
        """Tambahkan note ke tag index (partial chain)."""
        tag_node = TagNode(tag, note_node)
        if tag not in self.tag_index:
            self.tag_index[tag] = tag_node
        else:
            # Prepend ke chain tag tersebut
            tag_node.next = self.tag_index[tag]
            self.tag_index[tag] = tag_node

    # ----------------------------------------------------------
    # ADD TAG TO EXISTING NOTE
    # ----------------------------------------------------------
    def add_tag(self, title: str, tag: str):
        """Tambahkan tag baru ke note yang sudah ada."""
        note = self._find_by_title_alpha(title)
        if note is None:
            print(f"[!] Note '{title}' tidak ditemukan.")
            return
        if tag in note.tags:
            print(f"[!] Tag '{tag}' sudah ada di note '{title}'.")
            return
        note.tags.append(tag)
        self._register_tag(tag, note)
        self.sync_buffer.add("TAG_ADD", title)
        print(f"[+] Tag '{tag}' ditambahkan ke note '{title}'.")

    # ----------------------------------------------------------
    # DELETE NOTE
    # ----------------------------------------------------------
    def delete_note(self, title: str):
        """
        Hapus note dari SEMUA chain:
        - Chronological chain
        - Alphabetical chain
        - Semua tag chain yang terkait
        Wajib hapus dari semua chain sebelum dealokasi (Multi-Linked rule).
        """
        note = self._find_by_title_alpha(title)
        if note is None:
            print(f"[!] Note '{title}' tidak ditemukan.")
            return

        # Hapus dari chronological chain
        self._remove_from_chron(note)

        # Hapus dari alphabetical chain
        self._remove_from_alpha(note)

        # Hapus dari semua tag chain
        for tag in note.tags:
            self._remove_from_tag(tag, note)

        self.sync_buffer.add("DELETE", title)
        self.count -= 1
        print(f"[-] Note '{title}' berhasil dihapus.")

    def _remove_from_chron(self, node: NoteNode):
        if node.prev_chron:
            node.prev_chron.next_chron = node.next_chron
        else:
            self.head_chron = node.next_chron

        if node.next_chron:
            node.next_chron.prev_chron = node.prev_chron
        else:
            self.tail_chron = node.prev_chron

        node.prev_chron = node.next_chron = None

    def _remove_from_alpha(self, node: NoteNode):
        if node.prev_alpha:
            node.prev_alpha.next_alpha = node.next_alpha
        else:
            self.head_alpha = node.next_alpha

        if node.next_alpha:
            node.next_alpha.prev_alpha = node.prev_alpha
        else:
            self.tail_alpha = node.prev_alpha

        node.prev_alpha = node.next_alpha = None

    def _remove_from_tag(self, tag: str, target_note: NoteNode):
        if tag not in self.tag_index:
            return
        cur = self.tag_index[tag]
        prev = None
        while cur is not None:
            if cur.note_ref is target_note:
                if prev is None:
                    self.tag_index[tag] = cur.next
                    if self.tag_index[tag] is None:
                        del self.tag_index[tag]
                else:
                    prev.next = cur.next
                return
            prev = cur
            cur = cur.next

    # ----------------------------------------------------------
    # SEARCH / VIEW
    # ----------------------------------------------------------
    def _find_by_title_alpha(self, title: str):
        """Cari note berdasarkan judul di alphabetical chain."""
        cur = self.head_alpha
        target = title.lower()
        while cur is not None:
            if cur.title.lower() == target:
                return cur
            if cur.title.lower() > target:
                break   # early termination (chain sorted)
            cur = cur.next_alpha
        return None

    def view_chronological(self):
        """Tampilkan semua note dari yang TERLAMA ke TERBARU."""
        print("\n=== Notes (Chronological: Oldest → Newest) ===")
        cur = self.head_chron
        i = 1
        while cur is not None:
            print(f"  {i}. {cur.title}  | Tags: {cur.tags}")
            print(f"     Created: {cur.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            cur = cur.next_chron
            i += 1
        if i == 1:
            print("  (tidak ada note)")

    def view_alphabetical(self):
        """Tampilkan semua note urut A-Z."""
        print("\n=== Notes (Alphabetical: A → Z) ===")
        cur = self.head_alpha
        i = 1
        while cur is not None:
            print(f"  {i}. {cur.title}  | Tags: {cur.tags}")
            cur = cur.next_alpha
            i += 1
        if i == 1:
            print("  (tidak ada note)")

    def view_by_tag(self, tag: str):
        """Tampilkan semua note dengan tag tertentu (partial chain)."""
        print(f"\n=== Notes dengan Tag: '{tag}' ===")
        if tag not in self.tag_index:
            print(f"  (tidak ada note dengan tag '{tag}')")
            return
        cur = self.tag_index[tag]
        i = 1
        while cur is not None:
            print(f"  {i}. {cur.note_ref.title}  | All Tags: {cur.note_ref.tags}")
            cur = cur.next
            i += 1

    def view_sync_history(self):
        """Tampilkan riwayat perubahan dari circular buffer."""
        self.sync_buffer.display()

    def status(self):
        """Ringkasan status aplikasi."""
        print(f"\n=== Status ===")
        print(f"  Total Notes : {self.count}")
        print(f"  Total Tags  : {len(self.tag_index)}")
        print(f"  Tag List    : {list(self.tag_index.keys())}")


# ============================================================
# BAGIAN 4: DEMO / TESTING
# ============================================================

def main():
    print("=" * 55)
    print("   Note-Taking App - Advanced Linked Lists Demo")
    print("=" * 55)

    app = NoteTakingApp(sync_capacity=5)

    # --- Tambah beberapa note ---
    app.add_note("Belajar Python",
                 "Python adalah bahasa pemrograman serbaguna.",
                 tags=["python", "programming", "belajar"])

    app.add_note("Algoritma Sorting",
                 "Quick sort, merge sort, dan bubble sort.",
                 tags=["algoritma", "programming"])

    app.add_note("Catatan Rapat",
                 "Rapat Senin: diskusi progress proyek.",
                 tags=["rapat", "kerja"])

    app.add_note("Resep Nasi Goreng",
                 "Bahan: nasi, telur, kecap, bawang.",
                 tags=["masak", "belajar"])

    app.add_note("Linked List",
                 "Doubly, Circular, Multi-Linked Lists.",
                 tags=["algoritma", "programming", "belajar"])

    # --- Lihat status ---
    app.status()

    # --- View chronological ---
    app.view_chronological()

    # --- View alphabetical ---
    app.view_alphabetical()

    # --- View by tag ---
    app.view_by_tag("programming")
    app.view_by_tag("belajar")
    app.view_by_tag("masak")

    # --- Tambah tag ke note yang sudah ada ---
    app.add_tag("Catatan Rapat", "penting")
    app.view_by_tag("penting")

    # --- Hapus satu note ---
    app.delete_note("Resep Nasi Goreng")

    # --- View setelah delete ---
    app.view_alphabetical()

    # --- Lihat sync history ---
    app.view_sync_history()

    # --- Status akhir ---
    app.status()

    print("\n" + "=" * 55)
    print("  Demo selesai!")
    print("=" * 55)


if __name__ == "__main__":
    main()
