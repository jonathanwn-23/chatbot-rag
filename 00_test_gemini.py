import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
if not os.getenv('GEMINI_API_KEY'):
    raise SystemExit('Isi GEMINI_API_KEY di file .env terlebih dahulu.')

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
question = 'Berapa hari proses surat aktif kuliah di Akademik Demo?'
response = client.models.generate_content(
    model=os.getenv('GEMINI_MODEL', 'gemini-3.5-flash-lite'),
    contents=question,
)
print('Pertanyaan:', question)
print('Jawaban tanpa RAG:', response.text or '(Tidak ada teks jawaban)')