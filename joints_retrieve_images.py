import cv2
from datetime import timedelta

vidcap = cv2.VideoCapture('09.mp4')
success, image = vidcap.read()

frame = 1
fps=1/30

while success:
	cv2.imwrite("video_data09/image_{:06d}.jpg".format(frame), image)    
	success, image = vidcap.read()
	sec = frame*fps
	vremya = timedelta(seconds=sec)
	print('{:06d}'.format(frame), vremya)
	frame+=1
	
