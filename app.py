# Aplikasi Information Retrieval — Boolean Retrieval Model

# ============================================================
# TUGAS 2 - INFORMATION RETRIEVAL
# Boolean Retrieval Model
# ============================================================

# ------------------------------------------------------------
# 1. DATA KOLEKSI OBJEK
# ------------------------------------------------------------

objects = {
    1: "mahasiswa fasilkom universitas jember adalah mahasiswa hebat",
    2: "universitas jember memiliki 30.000 mahasiswa",
    3: "saat ini fasilkom universitas jember memiliki tiga prodi",
    4: "prodi pertama fasilkom universitas jember saat ini adalah prodi sistem informasi"
}


# ------------------------------------------------------------
# 2. REPRESENTASI OBJEK / TOKENISASI
# ------------------------------------------------------------

def tokenize(text):
    """
    Mengubah teks menjadi list of terms.
    """
    return text.lower().split()


documents = {}

for obj_id, text in objects.items():
    documents[obj_id] = tokenize(text)


print("=" * 70)
print("1. REPRESENTASI OBYEK")
print("=" * 70)

for obj_id, terms in documents.items():
    print(f"D{obj_id} = {terms}")


# ------------------------------------------------------------
# 3. MEMBANGUN DICTIONARY & INVERTED LIST
# ------------------------------------------------------------

inverted_index = {}

for doc_id, terms in documents.items():

    # set digunakan agar satu term hanya dicatat sekali
    # dalam dokumen yang sama.
    unique_terms = set(terms)

    for term in unique_terms:

        if term not in inverted_index:
            inverted_index[term] = []

        inverted_index[term].append(doc_id)


# Urutkan document ID pada setiap inverted list
for term in inverted_index:
    inverted_index[term].sort()


# Urutkan dictionary berdasarkan term
inverted_index = dict(sorted(inverted_index.items()))


print("\n" + "=" * 70)
print("2. DICTIONARY & INVERTED LIST")
print("=" * 70)

print(f"{'Dictionary':<20} {'Inverted List'}")
print("-" * 40)

for term, posting_list in inverted_index.items():
    print(f"{term:<20} {posting_list}")


# ------------------------------------------------------------
# 4. MEMBANGUN QUERY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. MEMBANGUN QUERY")
print("=" * 70)

query = input("Ketik yang anda cari: ").lower().strip()

theta = tokenize(query)

print(f"Theta: {theta}")


# ------------------------------------------------------------
# 5. MENCARI DOKUMEN YANG SESUAI DENGAN QUERY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. DOKUMEN YANG SESUAI DENGAN QUERY")
print("=" * 70)


def get_posting_list(term):
    """
    Mengambil inverted list dari sebuah term.
    Jika term tidak ditemukan, return list kosong.
    """
    return inverted_index.get(term, [])


posting_lists = {}

for i, term in enumerate(theta, start=1):

    posting_list = get_posting_list(term)

    posting_lists[term] = posting_list

    print(f"{term} (S {i} ): {posting_list}")


# ------------------------------------------------------------
# 6. BOOLEAN RETRIEVAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. RETRIEVED OBJECT (R)")
print("=" * 70)


# ------------------------------------------------------------
# AND
# ------------------------------------------------------------

def boolean_and(terms):
    """
    AND = irisan (intersection) dari posting list.
    """

    if not terms:
        return []

    result = set(get_posting_list(terms[0]))

    for term in terms[1:]:
        result = result.intersection(
            set(get_posting_list(term))
        )

    return sorted(result)


# ------------------------------------------------------------
# OR
# ------------------------------------------------------------

def boolean_or(terms):
    """
    OR = gabungan (union) dari posting list.
    """

    result = set()

    for term in terms:
        result = result.union(
            set(get_posting_list(term))
        )

    return sorted(result)


# ------------------------------------------------------------
# NOT
# ------------------------------------------------------------

def boolean_not(terms):
    """
    NOT digunakan sebagai:
    dokumen yang mengandung term pertama
    tetapi tidak mengandung term berikutnya.

    Contoh:
    mahasiswa NOT hebat

    [1,2] - [1] = [2]
    """

    if not terms:
        return []

    result = set(get_posting_list(terms[0]))

    for term in terms[1:]:
        result = result.difference(
            set(get_posting_list(term))
        )

    return sorted(result)


# ------------------------------------------------------------
# FUNGSI MENAMPILKAN HASIL RETRIEVAL
# ------------------------------------------------------------

def display_results(title, result):

    print("\n" + title)

    if not result:
        print("Tidak ada objek yang sesuai.")
        return

    for doc_id in result:
        print(f"Obj {doc_id} : {objects[doc_id]}")


# ------------------------------------------------------------
# HASIL AND
# ------------------------------------------------------------

and_result = boolean_and(theta)

display_results(
    'Retrieved object (R) dengan logika "AND"',
    and_result
)


# ------------------------------------------------------------
# HASIL OR
# ------------------------------------------------------------

or_result = boolean_or(theta)

display_results(
    'Retrieved object (R) dengan logika "OR"',
    or_result
)


# ------------------------------------------------------------
# HASIL NOT
# ------------------------------------------------------------

not_result = boolean_not(theta)

display_results(
    'Retrieved object (R) dengan logika "NOT"',
    not_result
)


print("\n" + "=" * 70)
print("PROGRAM SELESAI")
print("=" * 70)
