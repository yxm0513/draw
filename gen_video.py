import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import os


show_enable =  False
text_enable = True


def repeat(f, n, x):
    for i in range(n):
        f(x)

def add_text(img, txt):
    if text_enable:
        cv2.putText(img, txt, (30, 1000), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 255, 255), 2)
    else:
        pass

def show_image(img):
    if show_enable:
        cv2.imshow('image', img)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
    else:
        pass

def gen_video(imgs, size=(1920, 1080), filename='test.mp4'):
    FPS = 25
    seconds = 5
    radius = 150

    fourcc = VideoWriter_fourcc(*'avc1')
    video = VideoWriter(filename, fourcc, float(FPS), size)
    frame = np.random.randint(220, 221,
                              (size[1], size[0], 3),
                              dtype=np.uint8)

    add_text(frame, 'begining')
    repeat(video.write, FPS * seconds, frame)

    for img in imgs:
        info = img[0].shape
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        # if info[0] > size[0]:
        #     img = img[0:size[0], 0:info[1]]
        # if info[1] > size[1]:
        #     img = img[0:info[0], 0:size[1]]
        try:
            frame[0:info[0], 0:info[1]] = img[0]
            add_text(frame, img[1])
            repeat(video.write, FPS * seconds, frame)
        except:
            pass
    # moving
    img = cv2.imread('res/test.jpg')
    info = img.shape
    for i in range(0, 1080, 10):
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        try:
            frame[i:i+info[0],0:0+info[1]]=img
            add_text(frame, 'moving')
            video.write(frame)
        except:
            pass
    for i in range(0, 1920, 10):
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        try:
            frame[0:info[0],i:i+info[1]]=img
            add_text(frame, 'moving')
            video.write(frame)
        except:
            pass
    video.release()

def gen_images(image='res/test.jpg'):

    img=cv2.imread(image)
    info=img.shape
    height=info[0]
    weight=info[1]
    mode=info[2]
    print("height: %d weight: %d"%(height, weight))
    imgs = []
    show_image(img)
    print("resize")
    # resize
    to = [30, 60, 120, 480, 720, 1080]
    for i in to:
        dstHeight= i
        dstWeight=int(i / height  * weight)
        print("\t%d, %d" % (dstHeight, dstWeight))
        dst = cv2.resize(img, (dstHeight, dstWeight))
        imgs.append((dst, 'resize y: %d x: %d'% (dstHeight, dstWeight)))


    show_image(imgs[2])
    print("cut")
    # cut
    to = ['10:20,10:30', '300:445, 0:354', '0:250, 20:354', '100:200,100:300', '200:800,300:700']
    #img[y:y + h, x:x + w]
    for i in to:
        a,b = i.split(',')
        print("\t%s, %s" % (a, b))
        a1, a2 = a.split(':')
        b1, b2 = b.split(':')
        dst=img[int(a1):int(a2),int(b1):int(b2)]
        imgs.append((dst, 'cut %s' % (i)))

    print("rotate")
    #rotate
    to = [45, 90, 180, 225]
    for i in to:
        mat_rotate=cv2.getRotationMatrix2D((height*0.5,weight*0.5),i,1)    #center angle 3scale
        dst=cv2.warpAffine(img,mat_rotate,(height,weight))
        imgs.append((dst, 'rotate'))

    show_image(imgs[-1])
    show_image(imgs[-5])

    # merge
    print("merge")
    for i in [0.5, 1, 4, 8]:
        image = cv2.resize(img, (0, 0), None, 1/i, 1/i)

        grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        grey_3_channel = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

        vertical = np.vstack((image, grey_3_channel))
        info = vertical.shape
        height = info[0]
        weight = info[1]
        imgs.append((vertical, 'concat y: %d x: %d'% (height, weight)))
        horizontal = np.hstack((image, grey_3_channel))
        info = horizontal.shape
        height = info[0]
        weight = info[1]
        imgs.append((horizontal, 'concat y: %d x: %d'% (height, weight)))
        vertical_concat = np.concatenate((image, grey_3_channel), axis=0)
        info = vertical_concat.shape
        height = info[0]
        weight = info[1]
        imgs.append((vertical_concat, 'vertical_concat y: %d x: %d'% (height, weight)))
        horizontal_concat = np.concatenate((image, grey_3_channel), axis=1)
        info = horizontal_concat.shape
        height = info[0]
        weight = info[1]
        imgs.append((horizontal_concat, 'concat y: %d x: %d'% (height, weight)))

        show_image(imgs[-1])
    print("merge & resize")
    img = cv2.resize(img, (1920, int(1080 * weight /height)))
    for i in [2, 4, 8, 16, 32]:
        image = cv2.resize(img, (0, 0), None, 1/i, 1/i)
        m = image
        n = image
        for j in range(i):
            m = np.vstack((m, image))
            n = np.hstack((n, image))
        imgs.extend([(m, 'merge & resize'),(n, 'merge & resize')])

    # no face
    print("no face")
    noface = cv2.imread('res/error_face.jpg')
    imgs.append((noface, 'no face'))
    print("many face")
    # many people
    mulface = cv2.imread('res/mulperson.jpg')
    imgs.append((mulface, 'mul face'))

    img = cv2.resize(mulface, (1920, int(1080 * weight /height)))
    for i in [2, 4, 8, 16, 32]:
        image = cv2.resize(img, (0, 0), None, 1/i, 1/i)
        m = image
        n = image
        for j in range(i):
            m = np.vstack((m, image))
            n = np.hstack((n, image))
        imgs.extend([(m, 'merge & resize'), (n, 'merge & resize')])

    return imgs



if __name__ == '__main__':
    imgs = gen_images()
    gen_video(imgs)
    #os.system('ffmpeg -i test.avi -vcodec libx264 test.mp4;rm -rf test.avi')
