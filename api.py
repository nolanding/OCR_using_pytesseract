import os
from flask import Flask, render_template, request

# import our OCR function
from ocr import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = os.getcwd() + '/images/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('error.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('error.html', msg='No file selected')
        #improper file format
        if not allowed_file(file.filename):
            return render_template('error.html', msg='Please check the file extension. Only {} allowed'.format(ALLOWED_EXTENSIONS))
        #true case
        if file and allowed_file(file.filename):

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            # call the OCR function on it
            extracted_text = ocr_core(path)

            # extract the text and display it
            return render_template('result.html',
                                   msg='Successfully Processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()