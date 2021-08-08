from threading import Thread
import cv2
from time import strftime
import os



os.environ['SDL_VIDEO_CENTERED'] = '1'
cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL




class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

            # time.sleep(.01)

    def show_frame(self):

        # Display text on frames in main program
        cv2.putText(self.frame, strftime("%Y-%m-%d" + "  " + "%H:%M:%S"), (175, 475), font, 1, (255, 255, 0), 1,
                    cv2.LINE_8)
        cv2.putText(self.frame, 'LON : ', (5, 15), font, 1, (255, 255, 0), 1, cv2.LINE_8)
        cv2.putText(self.frame, 'LAT : ', (5, 35), font, 1, (255, 255, 0), 1, cv2.LINE_8)
        cv2.putText(self.frame, 'SPD : ', (5, 55), font, 1, (255, 255, 0), 1, cv2.LINE_8)
        cv2.putText(self.frame, 'BRG : ', (5, 75), font, 1, (255, 255, 0), 1, cv2.LINE_8)
        # Display Webcam Live Feed
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)


if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass
