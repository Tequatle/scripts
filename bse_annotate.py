import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from PIL import Image
import numpy as np
import os
from math import cos, sin, log
from random import choice, uniform

list_allFiles = os.listdir(os.getcwd()) #получить список всех файлов
dict_images = [] #

def get_hdr_data(hdr_filename):
    hdr_data = {}
    with open(hdr_filename, encoding='utf-8') as hdr:
        text = hdr.readlines()
        hdr_data['filename_hdr'] = hdr_fname
        hdr_data['Date'] = text[2][5:].strip() #2021-10-29
        hdr_data['ImageStripSize'] = int(text[6][15:].strip()) #полоса снизу в пикселях
        hdr_data['Magnification'] = float(text[7][14:].strip()) #0.0000e3
        hdr_data['PixelSizeX'] = float(text[9][11:].strip()) #размер пикселя
        hdr_data['ViewFieldsCountX'] = int(text[17][17:].strip()) #кол-во bse/se полей
        hdr_data['ViewFieldsCountY'] = int(text[18][17:].strip())
        hdr_data['StageRotation'] = float(text[58][14:].strip()) #поворот
        hdr_data['StageX'] = float(text[60][7:].strip()) #x
        hdr_data['StageY'] = float(text[61][7:].strip()) #y
        hdr_data['WD'] = text[67][3:].strip() #z
        #Добавить BSE/SE позиции кадров Detector0=BSE Detector1=SE
    return hdr_data

for fname in list_allFiles:
    #создать список файлов с расширениями *.tif, *.jpg, *.png
    if fname.endswith('tif') or fname.endswith('jpg') or fname.endswith('png'):
        #создать список файлов hdr
        fname_wo_ext, fname_extension = os.path.splitext(fname)
        hdr_fname = fname_wo_ext + '-' + fname_extension[1:] + '.hdr'
        #вытащить данные hdr файлов
        data = get_hdr_data(hdr_fname)
        #добавить имя файла с изображением
        data['filename'] = fname
        dict_images.append(data) 

fig, ax = plt.subplots()
ax.set_aspect(aspect=1)
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
for image in dict_images:
    im = Image.open(image['filename'])
    width_o, height_o = im.size
    #crop left, upper, right, lower
    im_crop = im.crop((width_o/image['ViewFieldsCountX'], 5, 2*width_o/image['ViewFieldsCountX'], height_o-image['ImageStripSize']))
    width = image['PixelSizeX'] * (width_o/image['ViewFieldsCountX']) * 1000
    height = image['PixelSizeX'] * (height_o-image['ImageStripSize']) * 1000
    angle = 3.14
    x = (image['StageX']*cos(angle) - image['StageY']*sin(angle)) * 1000
    y = (image['StageX']*sin(angle) + image['StageY']*cos(angle)) * 1000
    xa = (log(image['Magnification'])-2.4) / 10 + x
    ya = (24 - 3*log(image['Magnification'])) / 10 + y
    im_width = int(abs(width))
    im_height = int(abs(height))
    print(x,y, im_width, im_height)
    ax.scatter(x, y)
    rect = patches.Rectangle((x-width/2, y-height/2), width, height, edgecolor='r', fill=False)
    ax.annotate(image['filename'][:-4], (x, y), xycoords='data', xytext=(xa, ya), textcoords='data', 
        va='center', arrowprops=dict(arrowstyle="-"), bbox=bbox_props)
    #print(x,y, width, height, image['Magnification'])
    ax.add_patch(rect)
    #ab = AnnotationBbox(OffsetImage(im_crop, zoom=4/image['Magnification']), (x, y),  frameon=False)
    #ax.add_artist(ab)
    #ax.text(x, y, image['filename'])
    #im_resized = im_crop.resize((im_width, im_height))
    im = plt.imshow(im_crop, cmap=plt.cm.gray, interpolation='nearest', extent=(x-width/2, x+width/2, y-height/2, y+height/2))

plt.xlim(-30,30)
plt.ylim(-30,30)
plt.show()

