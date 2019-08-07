import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc


show =  False


def repeat(f, n, x):
    for i in range(n):
        f(x)
def show_image(img):
    if show:
        cv2.imshow('image', img)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
    else:
        pass

def gen_video(imgs, size=(1920, 1080), filename='test.avi'):
    FPS = 24
    seconds = 5
    radius = 150

    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter(filename, fourcc, float(FPS), size)

    for img in imgs:
        info = img.shape
        frame = np.random.randint(255, 256,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        frame[0:info[0], 0:info[1]] = img
        repeat(video.write, FPS * seconds, frame)

    video.release()

def gen_images(image='res/test.jpg'):

    img=cv2.imread(image)
    info=img.shape
    height=info[0]
    weight=info[1]
    mode=info[2]
    imgs = []
    show_image(img)
    print("resize")
    # resize
    to = [30, 60, 120, 480, 720, 1080]
    for i in to:
        dstHeight= i
        dstWeight=int(i / height  * weight)
        print("\t%d, %d" % (dstHeight, dstWeight))
        dst=cv2.resize(img,(dstHeight,dstWeight))
        imgs.append(dst)

    show_image(imgs[2])
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
    # print("mirror")
    # #mirror
    # dst=np.zeros(img.shape,np.uint8)
    # for i in range(height):
    #     for j in range(weight):
    #         dst[i,j]=img[height-i-1,j]
    # to = [30, 60, 120, 480, 720, 1080]
    # for i in to:
    #     dstHeight= i
    #     dstWeight=int(height /i * weight)
    #     dst=cv2.resize(img,(dstHeight,dstWeight))
    #     imgs.append(dst)
    print("rotate")
    #rotate
    to = [45, 90, 180, 225]
    for i in to:
        mat_rotate=cv2.getRotationMatrix2D((height*0.5,weight*0.5),i,1)    #center angle 3scale
        dst=cv2.warpAffine(img,mat_rotate,(height,weight))
        imgs.append(dst)

    show_image(imgs[-1])
    show_image(imgs[-5])

    # merge
    image = cv2.resize(img, (0, 0), None, .25, .25)

    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    grey_3_channel = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

    vertical = np.vstack((image, grey_3_channel))
    horizontal = np.hstack((image, grey_3_channel))

    vertical_concat = np.concatenate((image, grey_3_channel), axis=0)
    horizontal_concat = np.concatenate((image, grey_3_channel), axis=1)

    imgs.extend([vertical, horizontal, vertical_concat, horizontal_concat])
    show_image(imgs[-1])
    show_image(imgs[-3])
    return imgs

if __name__ == '__main__':
    imgs = gen_images()
    gen_video(imgs)
