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

def gen_video(size=(1920, 1080), filename='test.mp4'):
    FPS = 10
    seconds = 3

    fourcc = VideoWriter_fourcc(*'avc1')
    video = VideoWriter(filename, fourcc, float(FPS), size)
    frame = np.random.randint(220, 221,
                              (size[1], size[0], 3),
                              dtype=np.uint8)

    add_text(frame, 'begining')
    repeat(video.write, FPS * seconds, frame)

    src = walk_dir("../test/imagesresized/")
    for imgfile in src:
        print(imgfile + "\n")
        img = cv2.imread(imgfile)
        info = img.shape
        height = info[0]
        weight = info[1]
        print(info)
        if info[0] >=1080 or info[1] >= 1080:
            img = cv2.resize(img, (192, int(108 * weight / height)))
        x = (size[1] - info[0]) // 2
        y = (size[0] - info[1]) // 2
        x1 = size[1] - info[0]
        y1 = size[0] - info[1]

        temp = [(0, 0), (0, y), (0, y1), (x, 0), (x, y), (x, y1), (x1, 0), (x1, y), (x1, y1)]

        for i in temp:
            # many people
            frame = np.random.randint(220, 221,
                                      (size[1], size[0], 3),
                                      dtype=np.uint8)
            img = cv2.imread(imgfile)
            info = img.shape
            print(i)
            print(info)
            print(str(i[0]) + ":" + str(info[0] + i[0]) + "\n")
            print(str(i[1]) + ":" + str(info[1] + i[1]) + "\n")
            frame[i[0]:(info[0] + i[0]), i[1]:(info[1] + i[1])] = img
            repeat(video.write, FPS * seconds, frame)

        for i in range(0, 1080, 10):
            frame = np.random.randint(220, 221,
                                      (size[1], size[0], 3),
                                      dtype=np.uint8)
            print(i)
            print(info)
            try:
            #if i+info[0] <= 1080:
                frame[i:i+info[0],0:0+info[1]]=img
                add_text(frame, 'moving')
                video.write(frame)
            except:
                pass
        for i in range(0, 1920, 10):
            try:
            #if i+info[1] <= 1920:
                frame = np.random.randint(220, 221,
                                      (size[1], size[0], 3),
                                      dtype=np.uint8)
                frame[0:info[0],i:i+info[1]]=img
                add_text(frame, 'moving')
                video.write(frame)
            except:
                pass
    video.release()


def walk_dir(dir, topdown=True):
    imgs = []
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name.endswith('.jpg'):
                imgs.append(os.path.join(root, name))
    return imgs


if __name__ == '__main__':
    gen_video()
