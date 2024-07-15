from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io
import base64
import re

# Path to Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Route principale pour afficher le formulaire de téléchargement
@app.route('/form', methods=['GET'])
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

    # Analyser le texte extrait
    try:
        data = {
            'material': re.search(r'Material:\s*(.*)', extracted_text).group(1).strip(),
            'plant': re.search(r'Plant:\s*(.*)', extracted_text).group(1).strip(),
            'storage_location': re.search(r'Storage Location:\s*(.*)', extracted_text).group(1).strip(),
            'movement_type': re.search(r'Movement Type:\s*(.*)', extracted_text).group(1).strip(),
            'special_stock': re.search(r'Special Stock:\s*(.*)', extracted_text).group(1).strip(),
            'material_document': re.search(r'Material Document:\s*(.*)', extracted_text).group(1).strip(),
            'posting_date': re.search(r'Posting Date:\s*(.*)', extracted_text).group(1).strip(),
            'quantity_in_unit_of_entry': re.search(r'Quantity in Unit of Entry:\s*(.*)', extracted_text).group(1).strip(),
            'unit_of_entry': re.search(r'Unit of Entry:\s*(.*)', extracted_text).group(1).strip()
        }
    except AttributeError:
        return jsonify({'error': 'Unable to parse the extracted text.'}), 400

    # Réinitialiser le pointeur de fichier et encoder l'image en base64
    file.seek(0)
    image_base64 = base64.b64encode(file.read()).decode('utf-8')

    # Rendre le modèle avec le texte extrait
    return render_template('results.html', data=data, image_data=image_base64)

@app.route('/test', methods=['GET'])
def test():
    return 'Server is running!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Changer le numéro de port si nécessaire
