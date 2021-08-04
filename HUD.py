import cv2
import os
from GPS import *


os.environ['SDL_VIDEO_CENTERED'] = '1'

window_name = "window"
interframe_wait_ms = 30

cap = cv2.VideoCapture(0)

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
    ret, frame = cap.read()
    font = cv2.FONT_HERSHEY_SIMPLEX
            # (live feed, text, position,font, scale, BGR color)
    cv2.putText(frame, 'LONG : ', (5, 25), font, 0.25, (255, 144, 30), 1, cv2.LINE_4)
    cv2.putText(frame, 'LAT  : ', (5, 50), font, 0.25, (255, 144, 30), 1, cv2.LINE_4)

    if not ret:
        break
    cv2.imshow(window_name, frame)
    if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
