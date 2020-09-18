import os
from flask import Flask, render_template, request
from pymongo import MongoClient 

# import our OCR function
from ocr import ocr_core, logger

# define a folder to store and later serve the images
UPLOAD_FOLDER = os.getcwd() + '/images/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
database = client['site_users']  
collection = database.pan_details  

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    logger.info('home_page')
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            logger.info('File not found')
            return render_template('error.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            logger.info('File not found')
            return render_template('error.html', msg='No file selected')
        #improper file format
        if not allowed_file(file.filename):
            logger.info('Please check the file extension. Only {} allowed'.format(ALLOWED_EXTENSIONS))
            return render_template('error.html', msg='Please check the file extension. Only {} allowed'.format(ALLOWED_EXTENSIONS))
        #true case
        if file and allowed_file(file.filename):

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            logger.info('Copy of file saved')

            # call the OCR function on it and save or user details from mongodb
            extracted_text = ocr_core(path, collection)
            if(len(extracted_text) == 0):
                return render_template('error.html', msg='Unable to read image.')


            # extract the text and display it
            return render_template('result.html',
                                   msg='Successfully Processed',
                                   extracted_text=extracted_text)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()