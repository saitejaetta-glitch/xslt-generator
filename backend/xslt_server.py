from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/generate-xslt', methods=['POST'])
def generate_xslt():
    if 'spec' not in request.files:
        return jsonify({"error": "No spec file uploaded"}), 400

    spec_file = request.files['spec']
    filename = spec_file.filename

    output_format = request.form.get('outputExtension', 'txt')
    separator = request.form.get('separator', ',')
    include_headers = request.form.get('includeHeaders', 'no')
    has_dt = request.form.get('hasDT', 'no')

    try:
        # Extract text from PDF or Excel
        if filename.endswith('.pdf'):
            with pdfplumber.open(spec_file) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(spec_file)
            text = df.to_string()
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        # Build a basic XSLT response (stub)
        prompt = f"""
Generate an XSLT stylesheet that fulfills the following requirements:

- Output format: {output_format.upper()}
- Separator: {separator}
- Include headers: {include_headers}
- Document transformation (DT): {has_dt}

Specification content:
{text[:1500]}
"""

        # Replace this with real GPT integration later
        generated_xslt = f"""<!-- XSLT generated based on uploaded spec -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- TODO: Actual transformation rules -->
</xsl:stylesheet>
"""

        return jsonify({
            "xslt": generated_xslt,
            "prompt": prompt  # Optional: helpful for debugging
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
