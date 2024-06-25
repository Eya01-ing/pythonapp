from flask import Flask, request, render_template
from PIL import Image
import pytesseract
import io
import base64
import re

# Path to Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

@app.route('/form', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    # Read the uploaded image file
    image = Image.open(io.BytesIO(file.read()))
    
    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(image)

    # Parse the extracted text
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
        return {'error': 'Unable to parse the extracted text.'}, 400

    # Reset file pointer and encode the image to base64
    file.seek(0)
    image_base64 = base64.b64encode(file.read()).decode('utf-8')

    # Render the template with extracted text
    return render_template('results.html', data=data, image_data=image_base64)

@app.route('/test', methods=['GET'])
def test():
    return 'Server is running!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change port number if needed
