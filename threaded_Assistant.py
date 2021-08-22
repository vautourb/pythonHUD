import datetime
import os
import pathlib
import webbrowser
import threading
from queue import Queue
from requests import get
import wmi
import netifaces
import psutil
import pyautogui
import pyttsx3
import wikipedia
import speech_recognition as sr
import smtplib

import win32gui
import win32process
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import socket
import sys

user = "Blaine"

r = sr.Recognizer()
audio_queue = Queue()


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

    # setter method .[0]=male voice and
    # [1]=female voice in set Property.
    en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Brian22"
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


# start a new thread to recognize audio, while this thread focuses on listening


with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source))
            r.SAMPLE_RATE = 44000
            r.adjust_for_ambient_noise(source, duration=5)
            print()
            print("Active threads", threading.activeCount())
            print()
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass


recognize_thread = threading.Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
