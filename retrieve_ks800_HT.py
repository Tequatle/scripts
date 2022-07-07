import pandas as pd
import cv2
import pytesseract
import datetime
from os import listdir
import numpy as np
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'

ksize = (6, 6)
kernel = np.ones((2, 2),np.uint8)
kernel2 = np.ones((5, 5),np.uint8)
pts1 = np.float32([[24,0],[518,0],[0,185],[494,185]])
pts2 = np.float32([[0,0],[494,0],[0,185],[494,185]])
M = cv2.getPerspectiveTransform(pts1,pts2)

#imo = cv2.imread('./df1/20220317_113552.jpg', cv2.IMREAD_UNCHANGED)[102:132, 72:150]

def make_temp1(imo):
	#print(imo.shape)
	imo = cv2.warpPerspective(imo, M, (100, 30))
	
	resized = cv2.resize(imo, (500, 150), interpolation = cv2.INTER_AREA)
	blue = cv2.bitwise_not(resized[:,:,1])
	#blud = cv2.dilate(blue, kernel, iterations = 1)
	blur = cv2.blur(blue, ksize)

	#thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]
	#cv2.imshow('image', blue)
	#cv2.waitKey(500)
	eroded_img = cv2.dilate(blur, kernel, iterations = 7)
	#cv2.imshow('eroded', eroded_img)
	#cv2.waitKey(50)

	#image2 = cv2.blur(eroded_img, ksize)
	#cv2.imshow('blurred', image2)
	#cv2.waitKey(50)

	thresh = cv2.threshold(eroded_img, 85, 255, cv2.THRESH_BINARY)[1]
	#image2 = cv2.dilate(thresh, kernel, iterations = 1)

	cv2.imshow('thresh', thresh)
	cv2.waitKey(50)	
	#print(thresh.shape)
	#cv2.imwrite('kek.jpg', thresh)
	r1a, r2a, r3a, r4a = 85, 185, 285, 390

	r1i = thresh[0:925, 0:r1a]
	r1 = pytesseract.image_to_string(r1i, lang='lets', config=config).rstrip()
	cv2.imshow('r1i', r1i)
	cv2.waitKey(50)

	r2i = thresh[0:925, r1a:r2a]
	r2 = pytesseract.image_to_string(r2i, lang='lets', config=config).rstrip()
	cv2.imshow('r2i', r2i)
	cv2.waitKey(50)

	r3i = thresh[0:925, r2a:r3a]
	r3 = pytesseract.image_to_string(r3i, lang='lets', config=config).rstrip()
	cv2.imshow('r3i', r3i)
	cv2.waitKey(50)

	r4i = thresh[0:925, r3a:r4a]
	r4 = pytesseract.image_to_string(r4i, lang='lets', config=config).rstrip()
	cv2.imshow('r4i', r4i)
	cv2.waitKey(5000)
	print(r1,r2,r3,r4)

	try:
		text = int(r1.rstrip())*1000 + int(r2.rstrip())*100 + int(r3.rstrip())*10 + int(r4.rstrip())
	except ValueError:
		text = 0



	return text


imo = cv2.imread('./df1/20220317_110657.jpg', cv2.IMREAD_UNCHANGED)
regul = make_temp1(imo[102:132, 335:435])
print(regul)

'''
imglist = listdir("./df1")
cols = ['time', 'regul', 'control']
lst = []
a = 0
for i in imglist:
	a += 1
	imo = cv2.imread('./df1/' + i, cv2.IMREAD_UNCHANGED)
	#regul = make_temp1(imo[102:132, 50:150])
	control = make_temp1(imo[102:132, 335:435])
	print(i, 100*a/len(imglist), regul, control)
	lst.append([datetime.datetime.strptime(i[:-4], '%Y%m%d_%H%M%S'), regul, control])


df = pd.DataFrame(lst, columns=cols)
print(df)
df.to_excel('output1.xlsx')
'''



