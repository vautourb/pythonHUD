import subprocess
import Webcam_MultiThreading
import threaded_Assistant

process2 = subprocess.Popen(["python", "threaded_assistant.py"]) # Create and launch process pop.py using python interpreter
process1 = subprocess.Popen(["python", "Webcam_MultiThreading.py"])

process1.wait()
