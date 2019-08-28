#!/usr/bin/python
from PIL import Image
import os, sys

path = "./images"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        print(item)
        if os.path.isfile(os.path.join(path,item)) and item.endswith('.jpg'):
            im = Image.open(os.path.join(path,item))
            imResize = im.resize((300,300), Image.ANTIALIAS)
            imResize.save('./imagesresized/' + item, 'JPEG', quality=90)
resize()
