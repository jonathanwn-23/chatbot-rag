import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / '.env')
if not os.getenv('GEMINI_API_KEY'):
    raise SystemExit('Isi GEMINI_API_KEY di file .env terlebih dahulu.')

text = (BASE / 'knowledge' / 'panduan_layanan.txt').read_text(encoding='utf-8')
chunks = [item.strip() for item in text.split('\n\n') if item.strip()]
if not chunks:
    raise SystemExit('Dokumen kosong. Periksa file panduan_layanan.txt.')

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
result = client.models.embed_content(
    model='gemini-embedding-001',
    contents=chunks,
    config=types.EmbedContentConfig(task_type='RETRIEVAL_DOCUMENT'),
)
vectors = np.asarray([item.values for item in result.embeddings], dtype=np.float32)
if len(vectors) != len(chunks):
    raise RuntimeError('Jumlah vektor tidak sama dengan jumlah chunk.')

folder = BASE / 'index'
folder.mkdir(exist_ok=True)
np.save(folder / 'embeddings.npy', vectors)
metadata = {'embedding_model': 'gemini-embedding-001', 'source': 'panduan_layanan.txt',
            'chunks': [{'id': i + 1, 'text': text} for i, text in enumerate(chunks)]}
(folder / 'chunks.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Index berhasil dibuat: {len(chunks)} chunk, dimensi vektor {vectors.shape[1]}.')
print('File: index/chunks.json dan index/embeddings.npy')