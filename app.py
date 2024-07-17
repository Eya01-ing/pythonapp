from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io
import base64
import re
from flask_cors import CORS , cross_origin
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
cors = CORS(app, resources={r"/proxy-to-sap": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image = Image.open(io.BytesIO(file.read()))

    extracted_text = pytesseract.image_to_string(image)
    print("Texte extrait :", extracted_text)  

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

    file.seek(0)
    image_base64 = base64.b64encode(file.read()).decode('utf-8')

   
    return render_template('results.html', data=data, image_data=image_base64)

@app.route('/test', methods=['GET'])
def test():
    return 'Server is running!'
@app.route('/proxy-to-sap', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])

def proxy_to_sap():
    data = request.get_json()

    url = "https://14385865trial-trial.integrationsuitetrial-apim.us10.hana.ondemand.com/14385865trial/AI"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic sb-f1802272-ccd0-41e5-9df4-e79403f0c99a!b297017|it!b26655:351e9efe-8bf5-4bee-8172-51b67b2f99f6$_xv2TgE8YPiJePwC2nvErf9YLRziE4P7CBMYi8ooIFE='
    }

    try:
      response = requests.post(url, json=data, headers=headers)
      response.raise_for_status()
      return jsonify(response.json())
    except requests.exceptions.RequestException as e:
      return jsonify({'error': f'Failed to send data to SAP: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
