# chatbot-rag

Backend Python untuk chatbot layanan mahasiswa berbasis **RAG (Retrieval-Augmented Generation)**. Folder ini berisi kode Flask API, pembuatan embedding, retrieval, dan integrasi Gemini API. Dibuat untuk praktikum mata kuliah Kecerdasan Buatan.

> Dokumen di `knowledge/` adalah **dokumen contoh (dummy)**, bukan aturan resmi kampus.

## Cara Kerja Singkat

1. Dokumen `.txt` dipecah menjadi chunk (satu bagian dipisahkan satu baris kosong).
2. Setiap chunk diubah menjadi embedding dengan `gemini-embedding-001` dan disimpan di `index/`.
3. Saat ada pertanyaan, pertanyaan diubah menjadi embedding, lalu dicari 3 chunk paling mirip (cosine similarity, top-k = 3).
4. Chunk tersebut disisipkan ke prompt, lalu Gemini menyusun jawaban beserta rujukan `[D...]`.
5. Flask menyediakan hasilnya sebagai API untuk website PHP (`chatbot-web`).

## Struktur Folder

```
chatbot-rag/
  .env                  (pribadi, TIDAK diunggah)
  .env.example          contoh isi .env
  .gitignore
  requirements.txt
  00_test_gemini.py     tes Gemini API tanpa RAG
  01_preview_chunks.py  melihat hasil chunking
  02_build_index.py     membuat embedding dan index
  03_test_retrieval.py  tes retrieval
  04_test_rag.py        tes jawaban RAG lewat terminal
  rag_core.py           fungsi inti: get_client, retrieve, answer_with_rag
  api_app.py            Flask API (/api/health dan /api/chat)
  knowledge/
    panduan_layanan.txt sumber pengetahuan (9 chunk)
  index/                dibuat otomatis oleh 02_build_index.py
    chunks.json
    embeddings.npy
```

## Kebutuhan

- Python 3.12 atau versi kompatibel (praktikum ini juga berjalan pada Python 3.14)
- Gemini API key dari https://aistudio.google.com/apikey
- Koneksi internet (untuk embedding dan jawaban Gemini)

## Instalasi

1. Buka folder ini di terminal, lalu buat dan aktifkan virtual environment (Windows PowerShell):

   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Pasang library:

   ```
   python -m pip install -r requirements.txt
   ```

3. Salin `.env.example` menjadi `.env`, lalu isi dengan key milik sendiri:

   ```
   GEMINI_API_KEY=isi_api_key_anda
   GEMINI_MODEL=gemini-2.5-flash-lite
   ```

   Nama model bisa disesuaikan dengan model yang tersedia di akun Anda.

## Menjalankan

### 1. Uji bertahap lewat terminal

```
python 00_test_gemini.py        # tes Gemini tanpa RAG
python 01_preview_chunks.py     # harus menampilkan: Jumlah chunk: 9
python 02_build_index.py        # membuat index (cukup sekali)
python 03_test_retrieval.py     # tes retrieval
python 04_test_rag.py           # tanya jawab RAG
```

Jalankan `02_build_index.py` ulang **hanya jika** isi `knowledge/panduan_layanan.txt` berubah. Langkah ini memakai kuota API.

### 2. Menjalankan Flask API

```
python -m flask --app api_app run --debug --host 127.0.0.1 --port 5000
```

Biarkan terminal tetap terbuka. Cek di browser: http://127.0.0.1:5000/api/health

### 3. Menghubungkan ke website

Salin folder `chatbot-web` ke `htdocs` (XAMPP) atau `www` (Laragon), nyalakan Apache, lalu buka `http://localhost/chatbot-web/`. **Apache dan Flask harus aktif bersamaan.**

## Endpoint API

| Endpoint | Metode | Fungsi |
|---|---|---|
| `/api/health` | GET | Mengecek bahwa Flask berjalan |
| `/api/chat` | POST | Menerima `{"question": "..."}`, mengembalikan `{"answer": "...", "sources": ["D2", ...]}` |

Pertanyaan maksimal 500 karakter.

## Troubleshooting

| Gejala | Solusi |
|---|---|
| `ModuleNotFoundError` | Aktifkan `.venv`, lalu `python -m pip install -r requirements.txt` |
| `Index belum dibuat` | Jalankan `python 02_build_index.py` |
| Jumlah chunk bukan 9 | Pastikan hanya ada satu baris kosong antarbagian di `panduan_layanan.txt` |
| Gemini 404 | Ganti `GEMINI_MODEL` di `.env` ke model yang tersedia di akun Anda |
| Gemini 429 | Kuota habis, tunggu beberapa saat |
| `Cannot send a request, as the client has been closed` | Simpan client ke variabel dulu (`client = get_client()`), jangan memanggil `get_client().models...` langsung |
| `502 Flask tidak dapat dihubungi` dari website | Pastikan Flask berjalan di 127.0.0.1 port 5000 |

## Keamanan

- **Jangan pernah mengunggah file `.env`** atau menampilkan API key di screenshot, laporan, atau repository.
- API key hanya dipakai di backend Python. Browser dan PHP tidak mengetahuinya.
- Jangan menaruh folder ini di `htdocs`/`www`. Folder website dan backend harus terpisah.
- Jika key terlanjur tersebar, nonaktifkan dan buat key baru di Google AI Studio.

## Catatan

RAG tetap bisa menghasilkan jawaban yang keliru. Selalu cocokkan jawaban dan chunk rujukan `[D...]` dengan isi dokumen sumber.