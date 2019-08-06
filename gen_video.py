import cv2
import numpy as np

def gen_video(imgs, size=(1920, 1080), filename='test.mp4'):
    out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, size)
    for i in range(len(imgs)):
        out.write(imgs[i])
    out.release()

def gen_images(image='res/test.jpg'):

    img=cv2.imread(image,1)
    info=img.shape
    height=info[0]
    weight=info[1]
    mode=info[2]
    imgs = []
    print("resize")
    # resize
    to = [30, 60, 120, 480, 720, 1080]
    for i in to:
        dstHeight= i
        dstWeight=int(i / height  * weight)
        print("\t%d, %d" % (dstHeight, dstWeight))
        dst=cv2.resize(img,(dstHeight,dstWeight))
        imgs.append(dst)
    print("cut")
    # cut
    to = ['10:20,10:30', '100:200,100:300', '200:800,300:700']
    for i in to:
        a,b = i.split(',')
        print("\t%s, %s" % (a, b))
        a1, a2 = a.split(':')
        b1, b2 = b.split(':')
        dst=img[int(a1):int(a2),int(b1):int(b2)]
        imgs.append(dst)
    print("move")
    # move
    dst=np.zeros(img.shape,np.uint8)
    for i in range(height-200):
        for j in range(weight-100):
            dst[i+200,j+100]=img[i,j]
    print("mirror")
    #mirror
    dst=np.zeros(img.shape,np.uint8)
    for i in range(height):
        for j in range(weight):
            dst[i,j]=img[height-i-1,j]
    to = [30, 60, 120, 480, 720, 1080]
    for i in to:
        dstHeight= i
        dstWeight=int(height /i * weight)
        dst=cv2.resize(img,(dstHeight,dstWeight))
        imgs.append(dst)
    print("rotate")
    #rotate
    to = [45, 90, 180, 225]
    for i in to:
        mat_rotate=cv2.getRotationMatrix2D((height*0.5,weight*0.5),i,1)    #center angle 3scale
        dst=cv2.warpAffine(img,mat_rotate,(height,weight))
        imgs.append(dst)

    return imgs

if __name__ == '__main__':
    imgs = gen_images()
    imgs.extend(imgs)
    imgs.extend(imgs)
    imgs.extend(imgs)
    imgs.extend(imgs)
    imgs.extend(imgs)
    imgs.extend(imgs)
    imgs.extend(imgs)
    imgs.extend(imgs)
    gen_video(imgs)
