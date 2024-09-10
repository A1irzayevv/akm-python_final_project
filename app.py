from flask import Flask, render_template, request, send_file, abort
from flask_cors import CORS
from scraper import *
from ai import response_ai
from referenceopener import *
from report import generate_pdf, generate_docx, generate_markdown  # Import specific report functions
import os

app = Flask(__name__)
CORS(app)

# Get the base directory where the app is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORTS_FOLDER = os.path.join(BASE_DIR, 'reports')

# Ensure the 'reports' folder exists
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

# Uzeyir Alirzayev - The route '/' was created by me for handling home directory of our web app
@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == "POST"):
        id = request.form.get("cve")
        validation = Validator(id)
        if validation == False:
            data = fetchData(id)
            ai_response = response_ai(id)
            if type(data) is dict:
                open_cve_links(id, data["References"])
                return render_template('index1.html', data=data, ai_response = ai_response)
        else:
            return render_template('index1.html', error=validation)
    return render_template('index1.html')

@app.route('/download/<cve_id>', methods=['POST'])
@app.route('/download/<cve_id>', methods=['POST'])
def download(cve_id):
    download_type = request.form.get('downloadType')
    filename = f"{cve_id}.{download_type}"
    filepath = os.path.join(REPORTS_FOLDER, filename)

    # Fetch the CVE data and AI response
    data = fetchData(cve_id)
    ai_response = response_ai(cve_id)  # Fetch the AI-generated summary
    if data is None:
        return render_template('index1.html', error="Failed to fetch CVE data for download.")
    
    data['ai_response'] = ai_response  # Include AI response in data

    try:
        # Generate the file based on the selected type
        if download_type == 'pdf':
            generate_pdf(data, REPORTS_FOLDER, filename)
        elif download_type == 'docx':
            generate_docx(data, REPORTS_FOLDER, filename)
        elif download_type == 'md':
            generate_markdown(data, REPORTS_FOLDER, filename)
        else:
            return render_template('index1.html', error="Invalid download type.")

        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)

    except Exception as e:
        print(f"Error generating or sending file: {e}")
        return render_template('index1.html', error=f"An error occurred: {str(e)}")


if __name__ == '__main__':
    app.run()