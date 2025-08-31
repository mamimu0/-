from flask import Flask, request, jsonify, send_file, render_template
import os
from extract_kanji import get_kanji_with_reading, create_kanji_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-pdf', methods=['POST'])
def create_pdf():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    kanji_readings = get_kanji_with_reading(text)

    if not kanji_readings:
        return jsonify({'message': 'No kanji found.'}), 200

    output_filename = create_kanji_pdf(kanji_readings)

    if not output_filename:
        return jsonify({'error': 'PDF generation failed.'}), 500

    return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)