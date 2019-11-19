#!/usr/bin/python
from PIL import Image
import os, sys

path = "../test/images"
dirs = os.listdir( path )

wpercent = 0.6

def resize():
    for item in dirs:
        print(item)
        if os.path.isfile(os.path.join(path,item)) and item.endswith('.png'):
            im = Image.open(os.path.join(path,item))
            #imResize = im.resize((600,800), Image.ANTIALIAS)
            imResize = im.resize((int(im.size[0]*wpercent), int(im.size[1]*wpercent)), Image.ANTIALIAS)
            if not os.path.exists('../test/imagesresized/'):
                os.mkdir('../test/imagesresized/')
            imResize.save('../test/imagesresized/' + item, 'PNG', quality=90)
resize()
