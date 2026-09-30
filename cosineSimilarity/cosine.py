# ------------------------------------------------------------
# 1. DATA KOLEKSI OBJEK
# ------------------------------------------------------------

objects = {
    1: "mahasiswa fasilkom universitas jember adalah mahasiswa hebat. mahasiswa fasilkom universitas jember banyak memenangkan turnamen baik akademik maupun non akademik. mulai tahun pertama, mahasiswa fasilkom universitas jember telah menunjukkan semangat untuk maju yang sangat tinggi",
    2: "prodi pertama fasilkom universitas jember adalah prodi sistem informasi. prodi sistem informasi fasilkom universitas jember mulai menerima mahasiswa pada tahun 2009. prodi sistem informasi fasilkom universitas jember berdiri sebagai prodi setara fakultas, sehingga prodi sistem informasi ini tidak berada di bawah fakultas manapun saat itu",
    3: "prodi informatika fasilkom universitas jember memiliki matakuliah pilihan yang bernama STKI. matakuliah STKI ditawarkan untuk mahasiswa yang ingin mempelajari metode pencarian informasi dari sekumpulan dokumen teks yang merupakan data tidak terstruktur. matakuliah STKI ditawarkan pada semester 6. Saat ini matakuliah STKI ditempuh 24 mahasiswa"
}

# ------------------------------------------------------------
# 2. REPRESENTASI OBJEK / TOKENISASI
# ------------------------------------------------------------

def tokenize(text):
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

    if not terms:
        return []

    result = set(get_posting_list(terms[0]))

    for term in terms[1:]:
        result = result.difference(
            set(get_posting_list(term))
        )

    return sorted(result)


# ------------------------------------------------------------
# FUNGSI MENAMPILKAN HASIL RETRIEVAL (BOOLEAN)
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

# ------------------------------------------------------------
# 6. PERANGKINGAN DENGAN COSINE SIMILARITY
# ------------------------------------------------------------

from math import sqrt


def cosine_similarity(query_terms, doc_terms):

    # Gabungkan term query dan dokumen
    all_terms = set(query_terms) | set(doc_terms)

    # Membuat vektor berdasarkan frekuensi term (TF)
    query_vector = []
    doc_vector = []

    for term in all_terms:
        query_vector.append(query_terms.count(term))
        doc_vector.append(doc_terms.count(term))

    # Dot product
    dot_product = sum(
        q * d
        for q, d in zip(query_vector, doc_vector)
    )

    # Panjang vektor query
    query_magnitude = sqrt(
        sum(q ** 2 for q in query_vector)
    )

    # Panjang vektor dokumen
    doc_magnitude = sqrt(
        sum(d ** 2 for d in doc_vector)
    )

    # Menghindari pembagian dengan nol
    if query_magnitude == 0 or doc_magnitude == 0:
        return 0.0

    # Cosine Similarity
    return dot_product / (query_magnitude * doc_magnitude)


def rank_cosine_similarity(query_terms, documents):

    scores = {}

    for doc_id, doc_terms in documents.items():

        score = cosine_similarity(
            query_terms,
            doc_terms
        )

        if score > 0:
            scores[doc_id] = score

    # Urutkan skor dari terbesar ke terkecil
    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ranked


print("\n" + "=" * 70)
print("6. PERANGKINGAN DENGAN COSINE SIMILARITY")
print("=" * 70)

ranking = rank_cosine_similarity(
    theta,
    documents
)

if not ranking:

    print("Tidak ada dokumen yang relevan")

else:

    for peringkat, (doc_id, score) in enumerate(
        ranking,
        start=1
    ):

        print(
            f"{peringkat}. Obj {doc_id} "
            f"(skor: {score:.3f}) : "
            f"{objects[doc_id]}"
        )

if not ranking:
    print("Tidak ada dokumen yang relevan")
else:
    for peringkat, (doc_id, score) in enumerate(ranking, start=1):
        print(f"{peringkat}. Obj {doc_id} (skor: {score:.3f}) : {objects[doc_id]}")


print("\n" + "=" * 70)
print("PROGRAM SELESAI")
print("=" * 70)