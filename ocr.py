try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import logging
from pymongo import MongoClient 

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(asctime)s - %(lineno)d - %(message)s ')
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG) 



def ocr_core(file, collection):
    """
    This function will handle the core OCR processing of images.
    """
    # text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    # return text
    logger.info(file)
    image = cv2.imread(file)
    image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    logger.info('Image extracted')
    # # noise
    gray = cv2.medianBlur(thresh, 5)
    # apply OCR to it
    file_name = './images/' + "test.png"
    cv2.imwrite(file_name, gray)
    # Simple image to string
    data = pytesseract.image_to_string(Image.open(file_name)).split('\n')
    data = list(filter(lambda x: x !='', data))
    data = list(filter(lambda x: x !=' ', data))
    logger.info('data : ' + str(data))
    pan_details = {}
    user_details = {}
    try:
        # if('Permanent Account Number' not in data): #if document is other than pancard
        #     return pan_details

        if(len(data)>=6):
            pan_details['fathers_name']	= data[3]
            pan_details['name']	= data[2]
            pan_details['dob']	= data[4]
            pan_details['pan_number'] = data[6].split(' ')[0]
        logger.info('pan_details : ' + str(pan_details))
        user_details = {'name' : pan_details['name'],  'fathers_name' : pan_details['fathers_name'], 
                    'dob' :pan_details['dob'], '_id' : pan_details['pan_number']}
    except Exception as e:
        logger.debug('Unable to read image.')
        return pan_details
    try:                 
        collection.insert_one(user_details) 
        return pan_details
    except Exception as e:
        logger.error(e)
        cursor = collection.find({'_id':pan_details['pan_number']})
        for a in cursor:
            return a


if __name__ == '__main__':
    file_name = input()
    client = MongoClient("mongodb://localhost:27017/")
    database = client['site_users']  
    collection = database.pan_details  
    print(ocr_core(file_name,collection))

