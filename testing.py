import webview
import time

46.346940, -79.437160

from time import sleep
latitude = 46.346940
longitude = -79.437160
miniMapurl = ('https://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(longitude) + '&zoom=18&size=512x512&maptype=hybrid&key=AIzaSyDg0SwqnAZuPSr86Z8XlJk65atfFqLvAjw')

def change_url(window):
    # wait a few seconds before changing url:
    time.sleep(2)

    # change url:
    window.load_url(miniMapurl)


if __name__ == '__main__':
    window = webview.create_window(miniMapurl, x=3075, y=1450, width=512, height=512, on_top=True, frameless=True)
    webview.start(change_url, window)
# anything below this line will be executed after program is finished executing
pass


