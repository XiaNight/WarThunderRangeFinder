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
squadPing = cv2.imread('SquadPing.png')
selfArrow = cv2.imread('SelfArrow.png')

LT = cv2.imread('LT.png')
MT = cv2.imread('MT.png')
HT = cv2.imread('HT.png')
TD = cv2.imread('TD.png')
SPAA = cv2.imread('SPAA.png')

icon_template_gray = cv2.cvtColor(selfArrow, cv2.COLOR_BGR2GRAY)
mapSize = int(input("Input map size: "))
miniMapSize = 435
mapRation = mapSize / miniMapSize

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

        # Find the icon in the screenshot
        (screenshot, selfArrowCenter) = FindIcon(screenshot, selfArrow, True)
        (screenshot, squadPingCenter) = FindIcon(screenshot, squadPing, True)

        # Find Enemies Icons
        threashHold = 0.72
        (screenshot, HTs) = FindIcons(screenshot, HT, threashHold, True, (0, 0, 255))
        (screenshot, MTs) = FindIcons(screenshot, MT, threashHold, True, (0, 255, 255))
        (screenshot, TDs) = FindIcons(screenshot, TD, threashHold, True, (255, 0, 255))
        (screenshot, SPAAs) = FindIcons(screenshot, SPAA, threashHold, True, (255, 255, 0))
        (screenshot, LTs) = FindIcons(screenshot, LT, threashHold, True, (0, 255, 0))

        # Calculate Enemy Distances

        enemies = HTs + MTs + TDs + SPAAs + LTs
        enemyWithDistances = []
        for enemy in enemies:
        	d = int(CalculateDistance(selfArrowCenter, enemy) * mapRation)
        	enemyWithDistances.append({"Pos": enemy, "Distance": d})

        print(enemyWithDistances)

        distance = CalculateDistance(selfArrowCenter, squadPingCenter)
        convertedDistance = distance * mapRation

        json = {"Self": selfArrowCenter, "Squad": squadPingCenter, "Distance": convertedDistance, "Enemies": enemyWithDistances}

        SendMessage(ToJson(json))
        Speak(int(convertedDistance))

        # Show the result
        # imS = cv2.resize(screenshot[:,:,2], (1920, 1080))
        # cv2.imshow('Screenshot with matched icon', imS)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

CloseSocket()