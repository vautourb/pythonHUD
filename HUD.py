import cv2
import os
from GPS import get_gps_data

os.environ['SDL_VIDEO_CENTERED'] = '1'

window_name = "window"
interframe_wait_ms = 30

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
def hud():
    while cap.isOpened():

        longitude, latitude, cur_speed = get_gps_data()

        ret, frame = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        #print("Longitude : " + longitude + "°" + " Latitude : " + latitude + "°" + " Spd  : " + cur_speed + " Kmh")
        #       (live feed,        text,              position,font, scale,     BGR color)
        cv2.putText(frame, 'LONG : ' + longitude, (5, 25), font, 0.25, (255, 144, 30), 1, cv2.LINE_4)
        cv2.putText(frame, 'LAT  : ' + str.Parse(latitude), (5, 50), font, 0.25, (255, 144, 30), 1, cv2.LINE_4)
        cv2.putText(frame, 'SPD : ' + str(cur_speed), (5, 75), font, 0.25, (255, 144, 30), 1, cv2.LINE_4)
        cv2.putText(frame, 'BRG : ', (5, 100), font, 0.25, (255, 144, 30), 1, cv2.LINE_4)

        if not ret:
            break
        cv2.imshow(window_name, frame)
        if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
            break
# test
    cap.release()
    cv2.destroyAllWindows()
