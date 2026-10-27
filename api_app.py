from flask import Flask, jsonify, request

from rag_core import answer_with_rag

app = Flask(__name__)


@app.get('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'Flask RAG API'})


@app.post('/api/chat')
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get('question', '')).strip()
    if not question:
        return jsonify({'error': 'Pertanyaan tidak boleh kosong.'}), 400
    if len(question) > 500:
        return jsonify({'error': 'Pertanyaan maksimal 500 karakter.'}), 400
    try:
        result = answer_with_rag(question)
        source_ids = [f"D{item['id']}" for item in result['sources']]
        return jsonify({'answer': result['answer'], 'sources': source_ids})
    except Exception:
        app.logger.exception('Proses RAG gagal')
        return jsonify({'error': 'Chatbot sedang bermasalah. Periksa terminal Flask.'}), 500