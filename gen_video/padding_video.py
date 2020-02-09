import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

filename = '/Users/yangxinming/detect_with_mask_single_fast_padding.mp4'
source = '/Users/yangxinming/detect_with_mask_single_fast.mp4'

show_enable =  False
text_enable = True

FPS = 25
seconds = 3

def repeat(f, n, x):
    for i in range(n):
        f(x)

def add_text(img, txt):
    if text_enable:
        cv2.putText(img, txt, (30, 1000), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 255, 255), 2)
    else:
        pass

fourcc = VideoWriter_fourcc(*'avc1')
video = VideoWriter(filename, fourcc, float(FPS), (1920, 1080))
frame = np.random.randint(220, 221,
                          (1080, 1920, 3),
                          dtype=np.uint8)

add_text(frame, 'begining')
repeat(video.write, FPS * seconds, frame)
print('done : begin')

cap = cv2.VideoCapture(source)
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    video.write(frame)

print('done : video')

frame = np.random.randint(220, 221,
                          (1080, 1920, 3),
                          dtype=np.uint8)
add_text(frame, 'ending')
repeat(video.write, FPS * seconds, frame)
print('done : end')

cap.release()