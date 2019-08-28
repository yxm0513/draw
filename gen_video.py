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
    FPS = 10
    seconds = 5

    fourcc = VideoWriter_fourcc(*'avc1')
    video = VideoWriter(filename, fourcc, float(FPS), size)
    frame = np.random.randint(220, 221,
                              (size[1], size[0], 3),
                              dtype=np.uint8)

    add_text(frame, 'begining')
    repeat(video.write, FPS * seconds, frame)

    for img in imgs:
        info = img[0].shape
        x = (size[1] - info[0]) // 2
        y = (size[0] - info[1]) // 2
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        try:
            frame[x:(info[0] + x), y:(info[1] + y)] = img[0]
            add_text(frame, img[1])
            repeat(video.write, FPS * seconds, frame)
        except:
            print("failed to porcess ")
            frame = cv2.resize(img[0], (1080, 1920))
            add_text(frame, img[1])
            repeat(video.write, FPS * seconds, frame)


    mulface = cv2.imread('res/mulperson.jpg')
    info = mulface.shape
    x = (size[1] - info[0])//2
    y = (size[0] - info[1])//2
    x1 = size[1] - info[0]
    y1 = size[0] - info[1]

    temp = [(0, 0), (0, y), (0, y1), (x, 0), (x, y), (x, y1), (x1, 0), (x1, y), (x1, y1)]

    for i in temp:
        # many people
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        mulface = cv2.imread('res/mulperson.jpg')
        info = mulface.shape
        print(i)
        print(info)
        print(str(i[0]) + ":" + str(info[0] + i[0]) + "\n")
        print(str(i[1]) + ":" + str(info[1] + i[1]) + "\n")
        frame[i[0]:(info[0] + i[0]), i[1]:(info[1] + i[1])] = mulface
        repeat(video.write, FPS * seconds, frame)
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
            try:
                frame = np.random.randint(220, 221,
                                      (size[1], size[0], 3),
                                      dtype=np.uint8)
                frame[0:info[0],i:i+info[1]]=img
                add_text(frame, 'moving')
                video.write(frame)
            except:
                pass
    src = walk_dir("./src/")
    for imgfile in src:
        img = cv2.imread(imgfile)
        info = img.shape
        x = (size[1] - info[0]) // 2
        y = (size[0] - info[1]) // 2
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        try:
            frame[x:(info[0] + x), y:(info[1] + y)] = img
            repeat(video.write, FPS * seconds, frame)
        except:
            print("failed to porcess ")
            frame = cv2.resize(img, (1080, 1920))
            repeat(video.write, FPS * seconds, frame)
    video.release()

def gen_images(files=None):
    index = 0
    print("resize")
    imgs = []
    # resize
    to = [30, 60, 120, 480, 720, 1080]
    for i in to:
        img = cv2.imread(files[index])
        info = img.shape
        height = info[0]
        weight = info[1]
        mode = info[2]
        print("height: %d weight: %d" % (height, weight))
        show_image(img)
        dstHeight= i
        dstWeight=int(i / height  * weight)
        print("\t%d, %d" % (dstHeight, dstWeight))
        dst = cv2.resize(img, (dstHeight, dstWeight))
        imgs.append((dst, 'resize y: %d x: %d'% (dstHeight, dstWeight)))
        index += 1

    print("cut")
    # cut
    to = ['10:20,10:30', '300:445, 0:354', '0:250, 20:354', '100:200,100:300', '200:800,300:700']
    #img[y:y + h, x:x + w]
    for i in to:
        img = cv2.imread(files[index])
        info = img.shape
        height = info[0]
        weight = info[1]
        mode = info[2]
        print("height: %d weight: %d" % (height, weight))
        a,b = i.split(',')
        print("\t%s, %s" % (a, b))
        a1, a2 = a.split(':')
        b1, b2 = b.split(':')
        dst=img[int(a1):int(a2),int(b1):int(b2)]
        imgs.append((dst, 'cut %s' % (i)))
        index += 1

    print("rotate")
    #rotate
    to = [45, 90, 135, 180, 225, 270, 315]
    for i in to:
        img = cv2.imread(files[index])
        info = img.shape
        height = info[0]
        weight = info[1]
        mode = info[2]
        print("height: %d weight: %d" % (height, weight))
        mat_rotate=cv2.getRotationMatrix2D((height*0.5,weight*0.5),i,1)    #center angle 3scale
        dst=cv2.warpAffine(img,mat_rotate,(height,weight))
        imgs.append((dst, 'rotate'))
        index += 1

    show_image(imgs[-1])
    show_image(imgs[-5])

    # merge
    print("merge")
    for i in [0.5, 1, 4, 8]:
        img = cv2.imread(files[index])
        info = img.shape
        height = info[0]
        weight = info[1]
        mode = info[2]
        print("height: %d weight: %d" % (height, weight))

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

        index += 1

        show_image(imgs[-1])
    print("merge & resize")

    img = cv2.resize(img, (1920, int(1080 * weight /height)))
    for i in [0.25, 0.5, 1, 2, 4, 8, 16, 32]:
        img = cv2.imread(files[index])
        info = img.shape
        height = info[0]
        weight = info[1]
        mode = info[2]
        print("height: %d weight: %d" % (height, weight))
        image = cv2.resize(img, (0, 0), None, 1/i, 1/i)
        m = image
        n = image
        if int(i) > 1:
            for j in range(i):
                m = np.vstack((m, image))
                n = np.hstack((m, m))
        else:
            m = np.vstack((m, image))
            n = np.hstack((m, m))
        imgs.extend([(m, 'merge & resize'),(n, 'merge & resize')])
        index += 1

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


def walk_dir(dir, topdown=True):
    imgs = []
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name.endswith('.jpg'):
                imgs.append(os.path.join(root, name))
    return imgs


if __name__ == '__main__':
    files = walk_dir("./res/")
    imgs = gen_images(files)
    gen_video(imgs)