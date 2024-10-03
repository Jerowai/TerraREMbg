from flask import Flask, request, render_template, send_file
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
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    try:
        # Resmi oku
        input_image = Image.open(file)

        # Arka planı kaldır
        output_image = remove(input_image)

        # Çıktıyı hafızada tut
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)

        # İşlenmiş resmi geri gönder
        return send_file(output_buffer, mimetype='image/png', as_attachment=False)

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

