import cv2
import numpy as np
import pyautogui
import keyboard
import time
import threading

from Util import *
import SocketManager as Socket
from Interface import Interface
import TimerLoop as Timer

# Define the key to trigger the screenshot and icon matching
key = 'c'

# Load the icon template
selfArrow, squadPing, enemyMarks = LoadIcons()

# Constants
miniMapSize = 435
miniMapBbox = (2110, 990, 435, 435)

# Variables
mainTimer = None
interface = None
identifyBtnPressed = False

# Interface Components
mapSizeVar = None
gridSizeVar = None
gridCountVar = None
warningVar = None

def ConvertGridSizeToMapSize():
    gridSize = gridSizeVar.get()
    gridCount = gridCountVar.get()
    mapSizeVar.set(gridSize * gridCount)

def SetMapSize():
    global mapRatio
    size = mapSizeVar.get()
    if size < 100:
        print("Map size needs to be more than 100")
        return
    mapRatio = size / miniMapSize

def StopIdentification():
    if mainTimer != None:
        print("Identification Stops")
        mainTimer.stop()

def StopProgram():
    StopIdentification()
    Socket.CloseSocket()
    interface.window.quit()
    print("App stoped")

def MainLoop():
    if True:
        print("Identifing")
        # Tell Unity to Clear all things and wait a little bit

        # Take a screenshot
        screenshot = TakeScreenShot(miniMapBbox)

        success, json = IdentifyScreenshot(screenshot, selfArrow, squadPing, enemyMarks, mapRatio=mapRatio, DEBUG=False)

        if success == False:
            if not Socket.SendMessage("Clear"):
                warningVar.set("Socket not connected")
            # Speak("失敗")
            return

        if not Socket.SendMessage(ToJson(json)):
            warningVar.set("Socket not connected")

        # if json['D'] != 0:
        #     Speak(int(json['D']))
        # else:
        #     Speak("無標示點")

def StartProgram():
    global stopFlag, mainTimer
    SetMapSize()
    if mapSizeVar.get() < 100:
        print("Set the map size first!")
        return
    print("App Starting, Press {0} to start calculation".format(key))

    if mainTimer == None:
        mainTimer = Timer.RepeatedTimer(5, MainLoop)
    mainTimer.start()

def TryConnect():
    Socket.CloseSocket()
    warningVar.set("Reconnecting")
    if Socket.ConnectSocket():
        warningVar.set("")
    else:
        warningVar.set("Socket not connected")

if __name__ == "__main__":
    interface = Interface("Control Panel")
    interface.window.protocol("WM_DELETE_WINDOW", StopProgram)

    # Nav Bar Start Stop
    interface.add_button("Start", 1, 0, StartProgram)
    interface.add_button("Stop", 1, 1, StopIdentification)
    warningVar = interface.add_label("", 1, 2)
    interface.add_button("Reconnect", 1, 3, TryConnect)

    # Map size setting
    interface.add_label("Number:", 2, 0)
    mapSizeVar = interface.add_int_entry(2, 1)

    interface.add_label("Calculator:", 2, 2)
    interface.add_label("Grid Size:", 2, 3)
    gridSizeVar = interface.add_int_entry(2, 4)
    gridSizeVar.set(300)
    interface.add_button("-", 2, 5, lambda: gridSizeVar.set(gridSizeVar.get()-10))
    interface.add_button("+", 2, 6, lambda: gridSizeVar.set(gridSizeVar.get()+10))

    interface.add_label("Grid Count:", 2, 7)
    gridCountVar = interface.add_float_entry(2, 8)
    gridCountVar.set(7)
    interface.add_button("-", 2, 9, lambda: gridCountVar.set(round(gridCountVar.get()-0.1, 1)))
    interface.add_button("+", 2, 10, lambda: gridCountVar.set(round(gridCountVar.get()+0.1, 1)))
    interface.add_button("Set", 2, 11, ConvertGridSizeToMapSize)

    if not Socket.ConnectSocket():
        warningVar.set("Socket not connected")

    interface.run()