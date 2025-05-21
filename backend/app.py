# backend/app.py

import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from io import BytesIO
from master_server import process_image_distributed_bytes

app = Flask(__name__)
CORS(app)  # Cho phép mọi origin

@app.route('/convert', methods=['POST'])
def convert():
    # Hỗ trợ cả key 'file' (curl) và 'image' (frontend)
    img_file = request.files.get('file') or request.files.get('image')
    if not img_file:
        return jsonify({'error': 'No image uploaded'}), 400

    img_bytes = img_file.read()
    try:
        result_bytes = process_image_distributed_bytes(img_bytes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return send_file(BytesIO(result_bytes), mimetype='image/png')


if __name__ == '__main__':
    HOST = os.getenv('HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5006))
    app.run(host=HOST, port=FLASK_PORT)
