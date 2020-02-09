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
    seconds = 30

    fourcc = VideoWriter_fourcc(*'avc1')
    video = VideoWriter(filename, fourcc, float(FPS), size)
    frame = np.random.randint(220, 221,
                              (size[1], size[0], 3),
                              dtype=np.uint8)

    add_text(frame, 'begining')
    repeat(video.write, FPS * 5, frame)
    src = walk_dir("/Users/yangxinming/test/face/imagesresized/")
    for imgfile in src:
        print(imgfile + "\n")
        img = cv2.imread(imgfile)
        info = img.shape
        frame = np.random.randint(220, 221,
                                  (size[1], size[0], 3),
                                  dtype=np.uint8)
        try:
            frame[0:info[0], 0:info[1]] = img
            repeat(video.write, FPS * seconds, frame)
        except:
            print("failed to porcess ")
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
