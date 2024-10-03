from flask import Flask, request, jsonify, render_template
from humanfriendly.terminal import output
from rembg import remove
from PIL import Image
import io
from flask import send_file
import os
from flask import flask

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Heroku'dan gelen PORT'u kullan
    app.run(host='0.0.0.0', port=port)  # Heroku, dış bağlantıları dinlemek için host'u '0.0.0.0' olarak ayarlayın


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # Resmi oku
    input_image = file.read()

    # Arka planı kaldır
    output_image = remove(input_image)

    # İşlenmiş resmi kaydet
    output_path = 'output.png'
    with open(output_path, 'wb') as f:
        f.write(output_image)

    # İslenmiş resmi gönder
    return send_file(output_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
