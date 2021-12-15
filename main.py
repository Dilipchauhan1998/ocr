import os

import flask
from flask import jsonify, request
from werkzeug.utils import secure_filename

from ocr.main import extract_data
from ocr.main import read_templates
from ocr.main import input_mapping

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction " \
           "novels.</p> "


@app.route('/upload', methods=['post'])
def uploadDocForOcr():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('documents', filename))
        template = request.form.get('doc-type')
        templates = read_templates('templates/' + template)

        fileType = filename.rsplit('.', 1)[1].lower()

        if fileType == 'pdf':
            print("using gvision2 tool for pdf")
            inputModule = 'gvision2'
        if fileType == 'jpeg' or fileType == 'jpg' or fileType == 'png':
            print("using gvision2 tool for image")
            inputModule = 'gvision2'

        result = extract_data('documents/' + filename, templates=templates, input_module=input_mapping[inputModule])
        if result:
            return result
        else:
            return ""
        # else:
        #     if fileType == 'pdf':
        #         inputModule = 'tesseract5'
        #         result = extract_data('documents/' + filename, templates=templates,
        #                           input_module=input_mapping[inputModule])
        #         if result:
        #             return result
        #         return ""
        #     else:
        #         return ""

    else:
        resp = jsonify({'message': 'Allowed file types are pdf, png, jpg, jpeg'})
        resp.status_code = 400
        return resp


ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.run()
