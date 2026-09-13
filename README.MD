# Boolean Retrieval Model

Aplikasi sederhana berbasis Python yang mengimplementasikan **Boolean Retrieval Model** untuk mencari objek atau dokumen berdasarkan kata kunci (*term*) menggunakan operasi logika Boolean, yaitu AND, OR, dan NOT.

Aplikasi ini dibuat untuk memenuhi **Tugas 2 — Information Retrieval**.

## 📌 Deskripsi

Boolean Retrieval Model merupakan model dalam Information Retrieval yang menentukan relevansi suatu dokumen berdasarkan keberadaan atau ketidakberadaan kata tertentu di dalam dokumen.

Aplikasi ini menggunakan koleksi data berupa beberapa objek yang berkaitan dengan kegiatan bulan Agustus. Setiap objek diproses melalui beberapa tahapan:

1. Representasi objek dan tokenisasi.
2. Pembuatan dictionary dan inverted index.
3. Pembuatan query dari input pengguna.
4. Pengambilan inverted list berdasarkan query.
5. Proses Boolean Retrieval menggunakan AND, OR, dan NOT.
6. Penampilan objek yang sesuai dengan query.

## 🚀 Fitur

- Tokenisasi teks menjadi kumpulan term.
- Pembuatan dictionary dan inverted list.
- Pencarian term berdasarkan query pengguna.
- Operasi Boolean **AND**.
- Operasi Boolean **OR**.
- Operasi Boolean **NOT**.
- Penampilan objek yang sesuai dengan hasil pencarian.
- Penanganan term yang tidak ditemukan dalam koleksi.

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python 3
- **Library:** Tidak menggunakan library eksternal.
- **Konsep:** Information Retrieval, Tokenisasi, Dictionary, Inverted Index, dan Boolean Retrieval Model.

## 📂 Struktur Proyek

```text
boolean-retrieval/
│
├── main.py
└── README.md