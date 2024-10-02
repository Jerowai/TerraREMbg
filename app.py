from flask import Flask, request, jsonify, render_template
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Fotoğrafı aç ve arka planı kaldır
    input_image = Image.open(file.stream)
    output_image = remove(input_image)

    # İşlenen fotoğrafı geri döndür
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return (img_byte_arr, 200, {
        'Content-Type': 'image/png',
        'Content-Disposition': 'inline; filename=result.png'
    })


if __name__ == '__main__':
    app.run(debug=True)
