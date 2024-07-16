from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io
import base64
import re
from flask_cors import CORS
 
# Chemin vers l'exécutable Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
CORS(app)
 
# Route principale pour afficher le formulaire de téléchargement
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route pour gérer le téléchargement et l'extraction du texte
@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Lire le fichier image téléchargé
    image = Image.open(io.BytesIO(file.read()))

    # Effectuer l'OCR à l'aide de Tesseract
    extracted_text = pytesseract.image_to_string(image)
    print("Texte extrait :", extracted_text)  # Ajout pour le débogage

    # Analyser le texte extrait
    try:
        data = {
            'sndpor': re.search(r'SNDPOR:\s*(.*)', extracted_text).group(1).strip() if re.search(r'SNDPOR:\s*(.*)', extracted_text) else 'N/A',
            'mestyp': re.search(r'MESTYP:\s*(.*)', extracted_text).group(1).strip() if re.search(r'MESTYP:\s*(.*)', extracted_text) else 'N/A',
            'begin': re.search(r'BEGIN:\s*(.*)', extracted_text).group(1).strip() if re.search(r'BEGIN:\s*(.*)', extracted_text) else 'N/A',
            'rcvpor': re.search(r'RCVPOR:\s*(.*)', extracted_text).group(1).strip() if re.search(r'RCVPOR:\s*(.*)', extracted_text) else 'N/A',
            'mandt': re.search(r'MANDT:\s*(.*)', extracted_text).group(1).strip() if re.search(r'MANDT:\s*(.*)', extracted_text) else 'N/A',
            'segment_1': re.search(r'SEGMENT_1:\s*(.*)', extracted_text).group(1).strip() if re.search(r'SEGMENT_1:\s*(.*)', extracted_text) else 'N/A',
            'edi_dc40': re.search(r'EDI_DC40:\s*(.*)', extracted_text).group(1).strip() if re.search(r'EDI_DC40:\s*(.*)', extracted_text) else 'N/A',
            'segment_3': re.search(r'SEGMENT_3:\s*(.*)', extracted_text).group(1).strip() if re.search(r'SEGMENT_3:\s*(.*)', extracted_text) else 'N/A',
            'segment_2': re.search(r'SEGMENT_2:\s*(.*)', extracted_text).group(1).strip() if re.search(r'SEGMENT_2:\s*(.*)', extracted_text) else 'N/A',
            'mtart': re.search(r'MTART:\s*(.*)', extracted_text).group(1).strip() if re.search(r'MTART:\s*(.*)', extracted_text) else 'N/A',
            'e1maram': re.search(r'E1MARAM:\s*(.*)', extracted_text).group(1).strip() if re.search(r'E1MARAM:\s*(.*)', extracted_text) else 'N/A',
            'direct': re.search(r'DIRECT:\s*(.*)', extracted_text).group(1).strip() if re.search(r'DIRECT:\s*(.*)', extracted_text) else 'N/A',
            'matnr': re.search(r'MATNR:\s*(.*)', extracted_text).group(1).strip() if re.search(r'MATNR:\s*(.*)', extracted_text) else 'N/A',
            'ernam': re.search(r'ERNAM:\s*(.*)', extracted_text).group(1).strip() if re.search(r'ERNAM:\s*(.*)', extracted_text) else 'N/A',
            'rcvprn': re.search(r'RCVPRN:\s*(.*)', extracted_text).group(1).strip() if re.search(r'RCVPRN:\s*(.*)', extracted_text) else 'N/A',
            'e1maktm': re.search(r'E1MAKTM:\s*(.*)', extracted_text).group(1).strip() if re.search(r'E1MAKTM:\s*(.*)', extracted_text) else 'N/A',
            'sndprt': re.search(r'SNDPRT:\s*(.*)', extracted_text).group(1).strip() if re.search(r'SNDPRT:\s*(.*)', extracted_text) else 'N/A',
            'rcvprt': re.search(r'RCVPRT:\s*(.*)', extracted_text).group(1).strip() if re.search(r'RCVPRT:\s*(.*)', extracted_text) else 'N/A',
            'meins': re.search(r'MEINS:\s*(.*)', extracted_text).group(1).strip() if re.search(r'MEINS:\s*(.*)', extracted_text) else 'N/A',
            'sndprn': re.search(r'SNDPRN:\s*(.*)', extracted_text).group(1).strip() if re.search(r'SNDPRN:\s*(.*)', extracted_text) else 'N/A',
            'mbrsh': re.search(r'MBRSH:\s*(.*)', extracted_text).group(1).strip() if re.search(r'MBRSH:\s*(.*)', extracted_text) else 'N/A',
            'tabnam': re.search(r'TABNAM:\s*(.*)', extracted_text).group(1).strip() if re.search(r'TABNAM:\s*(.*)', extracted_text) else 'N/A',
            'idoctyp': re.search(r'IDOCTYP:\s*(.*)', extracted_text).group(1).strip() if re.search(r'IDOCTYP:\s*(.*)', extracted_text) else 'N/A',
            'container': re.search(r'CONTAINER:\s*(.*)', extracted_text).group(1).strip() if re.search(r'CONTAINER:\s*(.*)', extracted_text) else 'N/A',
        }
    except AttributeError as e:
        return jsonify({'error': f'Unable to parse the extracted text. Details: {e}'}), 400

    # Réinitialiser le pointeur de fichier et encoder l'image en base64
    file.seek(0)
    image_base64 = base64.b64encode(file.read()).decode('utf-8')

    # Rendre le modèle avec le texte extrait
    return render_template('results.html', data=data, image_data=image_base64)

@app.route('/test', methods=['GET'])
def test():
    return 'Server is running!'

if __name__ == '__main__':
    app.run(debug=True)
