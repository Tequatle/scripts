from PIL import Image
import pytesseract
import cv2
from datetime import timedelta
import os
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'

data = pd.DataFrame(columns=['name', 'time','ms', 'обороты', 'давление', 'dx', 'цикла'])

def thrshld(image):
	width = int(image.shape[1] * 2)
	height = int(image.shape[0] * 2)
	dsize = (width, height)
	image = cv2.resize(image, dsize)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.GaussianBlur(image,(7,1),1)
	image = cv2.threshold(image, 117, 255, cv2.THRESH_BINARY_INV)[1]
	return image

def get_loop(img):
	crop_img = img[930:971, 1267:1353] #loop
	textimage = thrshld(crop_img)
	text = pytesseract.image_to_string(textimage, lang='eng', config=config)
	return text

def get_spin(img):
	crop_img = img[953:975, 1786:1825] #spin
	textimage = thrshld(crop_img)
	text = pytesseract.image_to_string(textimage, lang='eng', config=config)
	return text

def get_pres(img):
	crop_img = img[985:1006, 1786:1825] #P
	textimage = thrshld(crop_img)
	text = pytesseract.image_to_string(textimage, lang='eng', config=config)
	return text

def get_xpos(img):
	crop_img = img[1015:1036, 1786:1825] #x
	textimage = thrshld(crop_img)
	text = pytesseract.image_to_string(textimage, lang='eng', config=config)
	return text


with os.scandir(r".\video_data16") as it:
	for entry in it:
		vseconds = int(entry.name[6:12])/30
		vremya = timedelta(seconds=vseconds)
		seconds = int(vremya.total_seconds())
		ms = "{:0>3}".format(str(vremya.microseconds)[:-3])
		image = cv2.imread(entry.path)
		s = get_spin(image).rstrip()
		p = get_pres(image).rstrip()
		x = get_xpos(image).rstrip()
		c = get_loop(image).rstrip()
		k = {'name':entry.name[6:12], 'time':seconds,'ms':ms, 'обороты':s, 'давление':p, 'dx':x, 'цикла':c}
		print(k)
		data = data.append(k, ignore_index=True)

data.to_csv('data16.csv')
print(data)
