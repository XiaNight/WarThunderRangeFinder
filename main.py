import cv2
import numpy as np
import pyautogui
import keyboard
import time

from Util import *
from SocketManager import *

# Define the key to trigger the screenshot and icon matching
key = 'c'
killKey = 'p'

# Load the icon template
selfArrow, squadPing, enemyMarks = LoadIcons()

mapSize = int(input("Input map size: "))

DEBUG = mapSize == -1
if mapSize < 100:
    print("Map size needs to be more than 100")
    mapSize = 1000

miniMapSize = 435
mapRatio = mapSize / miniMapSize

miniMapBbox = (2110, 990, 435, 435)

print("App Starting, Press {0} to start calculation, {1} to stop the program".format(key, killKey))


while True:
    time.sleep(0.1)
    if keyboard.is_pressed(killKey):
        break
    if keyboard.is_pressed(key):
        # Tell Unity to Clear all things and wait a little bit
        SendMessage("Clear")
        time.sleep(0.25)

        # Take a screenshot
        screenshot = TakeScreenShot(miniMapBbox)

        success, json = IdentifyScreenshot(screenshot, selfArrow, squadPing, enemyMarks, mapRatio=mapRatio, DEBUG=True)

        if success == False:
            SendMessage("Clear")
            Speak("失敗")
            continue

        SendMessage(ToJson(json))

        if json['D'] != 0:
            Speak(int(json['D']))
        else:
            Speak("無標示點")

        # Show the result
        if DEBUG:
            ShowImg(screenshot)

CloseSocket()
Speak("結束程式")