import datetime
import os
import webbrowser
from threading import Thread

import psutil
import pyautogui
import pyttsx3
import wikipedia

assistant = "Tombs"
user = "Blaine"

try:
    from queue import Queue  # Python 3 import
except ImportError:
    from Queue import Queue  # Python 2 import

import speech_recognition as sr


r = sr.Recognizer()
audio_queue = Queue()


def speak(audio):
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')

    # setter method .[0]=male voice and
    # [1]=female voice in set Property.
    engine.setProperty('voice', voices[0].id)

    # Method for the speaking of the the assistant
    engine.say(audio)

    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {user}")
    elif (hour >= 12) and (hour < 18):
        speak(f"Good afternoon {user}")
    elif (hour >= 18) and (hour < 21):
        speak(f"Good Evening {user}")
    speak("How may I assist you?")


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
    # nd then after slicing we can get time
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
            query = r.recognize_google(audio).lower( )
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))

            #speak("Google Speech Recognition thinks you said " + r.recognize_google(audio))

            if "open google" in query:
                speak("Opening google ")

                # in the open method we just to give the link
                # of the website and it automatically open
                # it in your default browser
                webbrowser.open("www.google.com")
                continue
            elif "what day is it" in query:
                tellDay()
                continue
            elif "tell me the time" in query:
                tellTime()
                continue
            elif "from wikipedia" in query:

                # if any one wants to have a information
                # from wikipedia
                speak("Checking the wikipedia ")
                query = query.replace("wikipedia", "")

                # it will give the summary of 4 lines from
                # wikipedia we can increase and decrease
                # it also.
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
                speak("Hold on " + user + ", I will show you where " + query[2] + " is.")
                maps_arg = webbrowser.open(location_url)
                os.system(maps_arg)
                continue
            elif "cpu" in query:
                speak(f"Cpu is at {str(psutil.cpu_percent())} percent")
                continue
            elif "ram" in query:
                ram_Used = psutil.virtual_memory()
                speak(f"RAM is at {str(ram_Used.percent)} percent")
                continue
#########################################################################
#
#                  WINDOWS COMMANDS
#
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
                ###############################################
                #
                #       ACTIVE VOICE WINDOWS 10 FUNCTIONS
                #          CONTROLS SCREEN LAYOUT
                #
                ###############################################

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
                ###############################################
                #
                #       ACTIVE VOICE DISPLAY WINDOW FUNCTIONS
                #          CONTROLS SCREEN LAYOUT
                #
                ###############################################


#########################################################################
#
#               WINDOWS PROGRAM OPTIONS
#

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
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source))
            # r.adjust_for_ambient_noise(source, duration=.05)
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop