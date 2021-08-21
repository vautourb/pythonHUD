import datetime
import os
import pathlib
import smtplib
import socket
import threading
import time
import webbrowser
from queue import Queue

import cv2
import googlemaps
import netifaces
import psutil
import pyautogui
import pyttsx3
import serial.tools.list_ports
import speech_recognition as sr
import webview
import wikipedia
import win32gui
import win32process
from requests import get
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp


user = "Blaine"

r = sr.Recognizer()
audio_queue = Queue()
# Google Maps info
gmaps = googlemaps.Client(key='AIzaSyAXyjUTd63knxXyHIpFhCuacMlUjIKwBos')

# Serial port variables
# AutoDetect Comports and Print Port name and Device Connected
print('Searching for COM Ports...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports:
    print('Found port : ' + port.device + " : " + str(port.hwid))
baud = 9600
serial_port = serial.Serial(port.device, baud, timeout=0)

# GPS Variables
latitude = 0
longitude = 0
cur_speed = 0
satLock = 0
LongitudeDegrees = 0
LatitudeDegrees = 0

# miniMap Variables

miniMapurl = ('https://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(
    longitude) + '&markers=icon:https://i.ibb.co/pZRVFfv/gmap-Team-Icon.png|&zoom=20&size=600x600&maptype=hybrid&key'
                 '=AIzaSyAXyjUTd63knxXyHIpFhCuacMlUjIKwBos')

def miniMap(window):
    # wait a few seconds before changing url:
    global miniMapurl
    while True:
        miniMapurl = ('https://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(
            longitude) + "&markers=icon:https://i.ibb.co/pZRVFfv/gmap-Team-Icon.png|&zoom=20&size=600x600&maptype"
                         "=hybrid&key=AIzaSyAXyjUTd63knxXyHIpFhCuacMlUjIKwBos")

        time.sleep(20)
        print("refreshed minimap again")

        # change url:
        window.load_url(miniMapurl)


# anything below this line will be executed after program is finished executing

pass



class camThread(threading.Thread):
    # Create a thread for each camera
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.previewName = previewName
        self.camID = camID

    # Open Available Cameras

    def run(self):
        print("Starting " + self.previewName)
        self.lock.acquire()
        camPreview(self.previewName, self.camID)
        self.lock.release()


# Show Cameras on ron and Process any edits to the stream


def camPreview(previewName, camID):
    global frame
    cv2.namedWindow(previewName, cv2.WND_PROP_FULLSCREEN)

    cam = cv2.VideoCapture(camID, cv2.CAP_DSHOW)
    if cam.isOpened():
        print("Main Cam Thread")
        cv2.setWindowProperty(previewName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        font = cv2.FONT_HERSHEY_DUPLEX
        today = datetime.datetime.now()

        date_time = today.strftime("%m/%d/%Y   %H:%M:%S.%f")[:-4]
        cv2.putText(frame, date_time, (225, 475), font, .4, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LON :' + " " + str(longitude) + " " + str(LongitudeDegrees), (5, 20), font, .4,
                    (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'LAT :' + " " + str(latitude) + " " + str(LatitudeDegrees), (5, 40), font, .4,
                    (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SAT :' + " " + str(satLock), (5, 60), font, .4, (0, 255, 255), 1, cv2.LINE_AA)
        # cv2.putText(frame, 'SPD :' + " " + str(cur_speed), (5, 80), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


# Create serial threads as follows


class serThread(threading.Thread):
    # Create a thread for each serial port
    def __init__(self, serName, serID):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.serName = serName
        self.serID = serID

    # Open Available Serial Ports

    def run(self):
        print("Starting " + self.serName)
        self.lock.acquire()
        read_from_port(serial_port)
        self.lock.release()


def read_from_port(ser):
    while True:

        global longitude
        global latitude
        global cur_speed
        global satLock
        global LongitudeDegrees
        global LatitudeDegrees

        try:

            ser_bytes = ser.readline()
            decoded_bytes = ser_bytes.decode("utf-8")
            data = decoded_bytes.split(",")

            if data[0] == '$GPRMC':
                # print("Received From COM5")
                # print(data)
                lat_nmea = data[3]
                lat_degrees = lat_nmea[:2]
                if data[4] == 'S':
                    latitude_degrees = float(lat_degrees) * -1
                else:
                    latitude_degrees = float(lat_degrees)
                    # Change it back to a string and remove the .0
                    latitude_degrees = str(latitude_degrees).strip('.0')
                    lat_ddd = lat_nmea[2:10]
                    lat_mmm = float(lat_ddd) / 60
                    lat_mmm = str(lat_mmm).strip('0.')[:6]
                    latitude = latitude_degrees + "." + lat_mmm
                    # Convert Longitude to decimal Coordinates
                    long_nmea = data[5]
                    long_degrees = long_nmea[1:3]
                    if data[6] == 'W':
                        longitude_degrees = float(long_degrees) * -1
                    else:
                        longitude_degrees = float(long_degrees)
                    # Change it back to a string and remove the .0
                    longitude_degrees = str(longitude_degrees).strip('.0')
                    long_ddd = long_nmea[3:10]
                    long_mmm = float(long_ddd) / 60
                    long_mmm = str(long_mmm).strip('0.')[:6]
                    longitude = longitude_degrees + "." + long_mmm

                    speed_nmea = data[7]
                    speed_kmh = float(speed_nmea) * 1.852
                    cur_speed = '{0:.1f}'.format(speed_kmh)

                    satLock = data[2]
                    LongitudeDegrees = data[6]
                    LatitudeDegrees = data[4]

                    print()
                    print("Active threads", threading.activeCount())
                    print("Sat Lock : " + satLock + " " + "Longitude : " + longitude + "°" + data[
                        6] + " Latitude : " + latitude + "°" + data[
                              4] + " Spd  : " + str(cur_speed) + " Km/h")
                    print()
        except:
            print()
            print("Active threads", threading.activeCount())
            # print("Lost Signal")


#################### cameras and gps above   ######    AI below




def speak(audio):
    engine = pyttsx3.init('sapi5')
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
    #    for voice in voices:
    #        print("Voice:")
    #        print(" - ID: %s" % voice.id)
    #        print(" - Name: %s" % voice.name)
    #        print(" - Languages: %s" % voice.languages)
    #        print(" - Gender: %s" % voice.gender)
    #        print(" - Age: %s" % voice.age)
    # default system voices below
    # setter method .[0]=male voice and
    # [1]=female voice in set Property.
    en_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\IVONA 2 Voice Brian22"
    engine.setProperty('voice', en_voice_id)
    newVoiceRate = 165
    engine.setProperty('rate', newVoiceRate)

    # Method for the speaking of the the assistant
    engine.say(audio)

    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()


speak("system is initializing!...")

speak("Running boot sequence!...")

speak("Updating databases!...")


def greet():
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0) and (hour < 12):
        speak(f"Good Morning! {user}")
    elif (hour >= 12) and (hour < 18):
        speak(f"Good afternoon! {user}")
    elif (hour >= 18) and (hour < 21):
        speak(f"Good Evening! {user}")
    # speak("How may I assist you?")


def tellDay():
    # This function is for telling the
    # day of the week
    day = datetime.datetime.today().weekday() + 1

    # this line tells us about the number
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)


def tellTime():
    # This method will give the time
    time = str(datetime.datetime.now())

    # the time will be displayed like
    # this "2020-06-05 17:50:14.582630"
    # and then after slicing we can get time
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak("The time sir is" + hour + "Hours and" + min + "Minutes")


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.zoho.com', 587)
    server.ehlo()
    server.starttls()
    server.login('blaine.vautour@bhconsultants.ca', '13Nmpv13')
    server.sendmail('blaine.vautour@bhconsultants.ca', to, content)
    server.close()


def recognize_worker():
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None:
            break  # stop processing if the main thread is done

        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            query = r.recognize_google(audio).lower()
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))

            # speak("Google Speech Recognition thinks you said " + r.recognize_google(audio))

            if "open google" in query:
                speak("Opening google ")
                webbrowser.open("www.google.com")
                continue
            elif "hello" in query:
                greet()
                continue
            elif "what day is it" in query:
                tellDay()
                continue
            elif "what time is it" in query:
                tellTime()
                continue
            elif "users" in query:
                users = psutil.users()
                for user in users:
                    speak("User" + str(user.name) + "on terminal" + str(user.terminal) + "from host" + str(user.host))
                continue
            elif "from wikipedia" in query:
                speak("Checking the wikipedia ")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=4)
                speak("According to wikipedia")
                speak(result)
                continue
            elif "search" in query:
                speak("what you want to search?")
                webbrowser.open("https://www.google.com/search?q=" + query)
                continue
            elif "medical" in query:
                query = query.replace("medical", "")
                stopwords = ['search', 'medical', 'definition', 'of', 'can', 'you', 'for']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)
                print(result)
                speak('Searching OpenMD' + result)
                webbrowser.open(url='https://openmd.com/define?q=' + result)
                continue
            elif "'open prime video" in query:
                speak('Opening Amazon Prime Video...')
                url = "https://www.primevideo.com/"
                webbrowser.open(url)
                continue
            elif "open netflix" in query:
                speak('Opening Netflix...')
                url = "netflix.com"
                webbrowser.open(url)
                continue
            elif "'open disney plus" in query:
                speak('Opening Disney Plus...')
                url = "https://www.disneyplus.com.com/"
                webbrowser.open(url)
                continue
            elif "where is" in query:
                query = query.split(" ")
                location_url = "https://www.google.com/maps/place/" + str(query[2])
                speak("Hold on I will show you where " + query[2] + " is.")
                maps_arg = webbrowser.open(location_url)
                os.system(maps_arg)
                continue

            #               system info commands

            elif "cpu" in query:
                speak(f"Cpu is at {str(psutil.cpu_percent())} percent")
                continue
            elif "ram" in query:
                ram_Used = psutil.virtual_memory()
                speak(f"RAM is at {str(ram_Used.percent)} percent")
                continue

            elif "total memory" in query:
                ram_Used = psutil.virtual_memory()
                ram_Total = ram_Used.total >> 30
                speak(f"My system has {ram_Total} Gigs of ram")
                continue

            elif "drive status" in query:
                disk = psutil.disk_usage('/')
                free = round(disk.free / 1024.0 / 1024.0 / 1024.0, 1)
                total = round(disk.total / 1024.0 / 1024.0 / 1024.0, 1)
                disk_info = str(free) + 'GigaBytes free / ' + str(total) + 'GigaBytes total ( ' + str(
                    disk.percent) + '% )'
                speak(str(free) + "GigaBytes free")
                speak(str(total) + "Total GigaBytes")
                continue

            #                  WINDOWS COMMANDS

            elif "lock computer" in query:
                pyautogui.keyDown('win')
                pyautogui.press('i')
                pyautogui.keyUp('win')
                continue
            elif "reboot" in query:
                query = query.replace("reboot", "")
                stopwords = ['reboot', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                os.system("shutdown /r /t 30")
                speak("I will reboot the system in 30 seconds")
                continue
            elif "abort" in query:
                query = query.replace("abort", "")
                stopwords = ['abort', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                os.system("shutdown /a")
                speak("Aborting system countdown!")
                continue

            #          ACTIVE VOICE WINDOWS 10 FUNCTIONS
            #          CONTROLS SCREEN LAYOUT

            elif "windows settings" in query:
                pyautogui.keyDown('win')
                pyautogui.press('c')
                pyautogui.keyUp('win')
                continue
            elif "action center" in query:
                pyautogui.keyDown('win')
                pyautogui.press('a')
                pyautogui.keyUp('win')
                continue

            #       ACTIVE VOICE DISPLAY WINDOW FUNCTIONS
            #          CONTROLS SCREEN LAYOUT

            elif "minimize" in query:
                query = query.replace("minimize", "")
                stopwords = ['minimize', 'to', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                strCmd = result
                # map type, the key value is the process ID, and the value is the window handle.
                mID2Handle = {}
                # print(strCmd)
                pro_found = [False]

                def get_all_hwnd(hwnd, mouse, pro_found):
                    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                        nID = win32process.GetWindowThreadProcessId(hwnd)
                        print(nID, win32gui.GetWindowText(hwnd))
                        # del nID[0]
                        if nID is not None:
                            print("\n{}\n".format(nID))
                        for abc in nID:
                            try:
                                pro = psutil.Process(abc).name().lower()
                                print(pro)
                            except psutil.NoSuchProcess:
                                print("no such process: {strCmd}")
                                pass
                            else:
                                print(abc, win32gui.GetWindowText(hwnd))
                                if strCmd in pro:
                                    pro_found[0] = True
                                    print("Process ID:", abc, "window handle: ", hwnd, " title: ",
                                          win32gui.GetWindowText(hwnd))
                                    mID2Handle[abc] = hwnd
                                    win32gui.ShowWindow(hwnd, 6)
                                    win32gui.SetForegroundWindow(hwnd)
                                    win32gui.SetActiveWindow(hwnd)

                win32gui.EnumWindows(lambda hwnd, mouse: get_all_hwnd(hwnd, mouse, pro_found), 0)
                if pro_found[0] is False:
                    speak("could not find{}".format(strCmd))
                continue

            elif "maximize" in query:
                query = query.replace("maximize", "")
                stopwords = ['maximize', 'to', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                strCmd = result
                # map type, the key value is the process ID, and the value is the window handle.
                mID2Handle = {}
                # print(strCmd)
                pro_found = [False]

                def get_all_hwnd(hwnd, mouse, pro_found):
                    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                        nID = win32process.GetWindowThreadProcessId(hwnd)
                        print(nID, win32gui.GetWindowText(hwnd))
                        # del nID[0]
                        if nID is not None:
                            print("\n{}\n".format(nID))
                        for abc in nID:
                            try:
                                pro = psutil.Process(abc).name().lower()
                                print(pro)
                            except psutil.NoSuchProcess:
                                print("no such process: {strCmd}")
                                pass
                            else:
                                print(abc, win32gui.GetWindowText(hwnd))
                                if strCmd in pro:
                                    pro_found[0] = True
                                    print("Process ID:", abc, "window handle: ", hwnd, " title: ",
                                          win32gui.GetWindowText(hwnd))
                                    mID2Handle[abc] = hwnd
                                    win32gui.ShowWindow(hwnd, 3)
                                    win32gui.SetForegroundWindow(hwnd)
                                    win32gui.SetActiveWindow(hwnd)

                win32gui.EnumWindows(lambda hwnd, mouse: get_all_hwnd(hwnd, mouse, pro_found), 0)
                if pro_found[0] is False:
                    speak("could not find{}".format(strCmd))
                continue

            elif "switch to" in query:
                query = query.replace("switch", "").replace("to", "")
                stopwords = ['switch', 'to', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                strCmd = result
                # map type, the key value is the process ID, and the value is the window handle.
                mID2Handle = {}
                # print(strCmd)
                pro_found = [False]

                def get_all_hwnd(hwnd, mouse, pro_found):
                    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                        nID = win32process.GetWindowThreadProcessId(hwnd)
                        print(nID, win32gui.GetWindowText(hwnd))
                        # del nID[0]
                        if nID is not None:
                            print("\n{}\n".format(nID))
                        for abc in nID:
                            try:
                                pro = psutil.Process(abc).name().lower()
                                print(pro)
                            except psutil.NoSuchProcess:
                                print("no such process: {strCmd}")
                                pass
                            else:
                                print(abc, win32gui.GetWindowText(hwnd))
                                if strCmd in pro:
                                    pro_found[0] = True
                                    print("Process ID:", abc, "window handle: ", hwnd, " title: ",
                                          win32gui.GetWindowText(hwnd))
                                    mID2Handle[abc] = hwnd
                                    win32gui.ShowWindow(hwnd, 9)
                                    win32gui.SetForegroundWindow(hwnd)
                                    win32gui.SetActiveWindow(hwnd)

                win32gui.EnumWindows(lambda hwnd, mouse: get_all_hwnd(hwnd, mouse, pro_found), 0)
                if pro_found[0] is False:
                    speak("could not find{}".format(strCmd))
                continue

            elif "top left corner" in query:
                query = query.replace("top", "").replace("left", "")
                stopwords = ['top', 'corner', 'window', 'left', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                strCmd = result
                # map type, the key value is the process ID, and the value is the window handle.
                mID2Handle = {}
                # print(strCmd)
                pro_found = [False]

                def get_all_hwnd(hwnd, mouse, pro_found):
                    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                        nID = win32process.GetWindowThreadProcessId(hwnd)
                        print(nID, win32gui.GetWindowText(hwnd))
                        # del nID[0]
                        if nID is not None:
                            print("\n{}\n".format(nID))
                        for abc in nID:
                            try:
                                pro = psutil.Process(abc).name().lower()
                                print(pro)
                            except psutil.NoSuchProcess:
                                print("no such process: {strCmd}")
                                pass
                            else:
                                print(abc, win32gui.GetWindowText(hwnd))
                                if strCmd in pro:
                                    pro_found[0] = True
                                    print("Process ID:", abc, "window handle: ", hwnd, " title: ",
                                          win32gui.GetWindowText(hwnd))
                                    win32gui.MoveWindow(hwnd, 0 - 7, 0, 1920, 1080, True)
                                    mID2Handle[abc] = hwnd
                                    win32gui.ShowWindow(hwnd, 9)
                                    win32gui.SetForegroundWindow(hwnd)
                                    win32gui.SetActiveWindow(hwnd)

                win32gui.EnumWindows(lambda hwnd, mouse: get_all_hwnd(hwnd, mouse, pro_found), 0)
                if pro_found[0] is False:
                    speak("could not find{}".format(strCmd))
                continue

            #           NETWORKING

            elif "what is my external ip" in query:
                speak("Attempting to get external ip")
                ip = get('https://api.ipify.org').text
                speak('My public IP address is: {}'.format(ip))
                continue

            elif "network discovery" in query:
                speak("Searching for active network devices")
                query = query.replace("scan network", "")
                stopwords = ['scan network', 'close', 'search', 'can', 'you']
                querywords = query.split()
                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords).strip()
                speak("Pinging devices")
                gateways = netifaces.gateways()
                default_gateway = gateways['default'][netifaces.AF_INET][0]
                target_ip = default_gateway + "/24"
                arp = ARP(pdst=target_ip)
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                packet = ether / arp
                result = srp(packet, timeout=3, verbose=0)[0]
                clients = []
                speak("Waiting for devices to respond")
                for sent, received in result:
                    # for each response, append ip and mac address to `clients` list
                    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

                # print clients

                print("Available devices in the network: {}".format(len(clients)))
                for client in clients:
                    try:
                        host_name = socket.gethostbyaddr(client["ip"])
                    except socket.herror as e:
                        print("Problem with ip: {}".format(client["ip"]))
                        client["host_name"] = "Unknown"
                        continue

                    print(host_name)
                    client["host_name"] = host_name[0]

                file_name = "NetworkReachableIP.csv"
                save_file_path = os.path.join(pathlib.Path(__file__).parent.absolute(), "", "db", "Network", file_name)
                with open(save_file_path, "w") as fs:
                    for client in clients:
                        fs.write("{0},{1},{2}\n".format(client['ip'], client['mac'], client["host_name"]))
                speak("Network devices discovered: {}".format(len(clients)))
                speak("The IP address, Mac Address and Hostnames have been recorded to the database")
                continue

            #               WINDOWS PROGRAM OPTIONS

            elif "show desktop" in query:
                pyautogui.keyDown('win')
                pyautogui.press('d')
                pyautogui.keyUp('win')
                continue
            elif "hide desktop" in query:
                pyautogui.keyDown('win')
                pyautogui.press('d')
                pyautogui.keyUp('win')
                continue
            elif "move down" in query:
                pyautogui.keyDown('win')
                pyautogui.press('down')
                pyautogui.keyUp('win')
                pyautogui.press('escape')
                continue
            elif "move up" in query:
                pyautogui.keyDown('win')
                pyautogui.press('up')
                pyautogui.keyUp('win')
                pyautogui.press('escape')
                continue
            elif "new virtual desktop" in query:
                pyautogui.keyDown('win')
                pyautogui.keyDown('ctrl')
                pyautogui.press('d')
                pyautogui.keyUp('win')
                pyautogui.keyDown('ctrl')
                continue
            # Move window multi monitor
            elif "move screen right" in query:
                pyautogui.keyDown('win')
                pyautogui.keyDown('shift')
                pyautogui.press('right')
                pyautogui.keyUp('win')
                pyautogui.keyUp('shift')
                continue
            elif "move screen left" in query:
                pyautogui.keyDown('win')
                pyautogui.keyDown('shift')
                pyautogui.press('left')
                pyautogui.keyUp('win')
                pyautogui.keyUp('shift')
                continue
            # more windows options
            elif "file explorer" in query:
                pyautogui.keyDown('win')
                pyautogui.press('e')
                pyautogui.keyUp('win')
                continue
            elif "windows search" in query:
                pyautogui.keyDown('win')
                pyautogui.press('s')
                pyautogui.keyUp('win')
                continue
            elif "take screenshot" in query:
                pyautogui.press('printscreen')
                continue


            #########################################################################
            #
            #               EMAIL
            #

            elif "send email" in query:
                try:
                    speak("What should I say?")
                    content = query()
                    to = "vautourb@live.com"
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry my friend. I am not able to send this email")
                continue

            #########################################################################
            #
            #           QUIT PROGRAM
            #
            elif "offline" in query:
                hour = datetime.datetime.now().hour
                if (hour >= 21) and (hour < 6):
                    speak(f"Good Night {user}! Have a good evening!")
                else:
                    speak(f"System going offline {user}")
                quit()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        audio_queue.task_done()  # mark the audio processing job as completed in the queue

with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source))
            r.SAMPLE_RATE = 44000
            r.adjust_for_ambient_noise(source, duration=5)
            print()
            print("Active threads", threading.activeCount())
            print("Running Threads", )
            print(threading.currentThread().getName(), 'Starting')
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass




print()
print("Active threads", threading.activeCount())
print()

if __name__ == '__main__':
    # mini Map window location with size
    window = webview.create_window('miniMap', miniMapurl, x=3075, y=1450, width=512,
                                   height=512, on_top=True, frameless=True)
    webview.start(miniMap, window)

##########################################################

# Camera Threads

thread1 = camThread("Main Cam", 0)  # Primary Camera
thread2 = camThread("IR Cam", 1)  # IR Camera
thread3 = camThread("Thermal Cam", 2)  # Thermal Camera
thread4 = camThread("NV Cam", 3)  # Night Vision Camera

# Serial Port Threads
thread5 = serThread("USB GPS", serial_port)
thread5.setDaemon(True)

# Camera Threads Start
thread1.start()
#thread1.join()
# thread2.start()
# thread3.start()
# thread4.start()

# Serial Port Threads Start
thread5.start()
thread5.join()


# start a new thread to recognize audio, while this thread focuses on listening
thread8 = threading.Thread("Recognizer", target=recognize_worker)
thread8.daemon = True
thread8.start()



audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
thread8.join()  # wait for the recognize_thread to actually stop
###############################