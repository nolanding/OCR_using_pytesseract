try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2


def ocr_core(file):
    """
    This function will handle the core OCR processing of images.
    """
    # text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    # return text
    print(file)
    print('im in ocr')
    image = cv2.imread(file)
    image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    # # noise
    gray = cv2.medianBlur(thresh, 5)
    # apply OCR to it
    file_name = './images/' + "test.png"
    cv2.imwrite(file_name, gray)
    # Simple image to string
    data = pytesseract.image_to_string(Image.open(file_name)).split('\n')
    data = list(filter(lambda x: x !='', data))
    data = list(filter(lambda x: x !=' ', data))
    pan_details = {}
    if(len(data)>=6):
    	pan_details['fathers_name']	 = data[3]
    	pan_details['name']	= data[2]
    	pan_details['dob']	= data[4]
    	pan_details['pan_number'] = data[6].split(' ')[0]
    print(pan_details)
    return pan_details


if __name__ == '__main__':
	file_name = input()
	print(ocr_core(file_name))