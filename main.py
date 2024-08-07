#!/usr/bin/env python3

import cv2
import os.path
from ppadb.client import Client
import numpy as np
import time
import argparse
import sys

HAND_MAIN_MIN = 0.52
HAND_MAIN_TYPE = cv2.TM_CCOEFF

HAND_CHEST_MIN = 0.19

GREEN_BTN_MIN = 0.9
GREEN_BTN_TYPE = cv2.TM_CCORR_NORMED

X_MIN = 0

parser = argparse.ArgumentParser("main.py")
parser.add_argument("type", help="which img to detecct and click", type=str)
args = parser.parse_args()

def findImg(path,  imgName, threshold, normalizer=1, clickPos= 'xy', type=1):
    if not threshold or not imgName:    
        return None
    
    img = sys.path[0] + '/img/neddle/' + imgName + '.png'

    printImg = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    needle = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(printImg, needle, type)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    clickOn = max_loc
    if clickPos == 'center':
        clickOn = [max_loc[0] + (needle.shape[1] / 2), max_loc[1] + (needle.shape[0] / 2)]

    if round(max_val / normalizer, 2) >= threshold:
        return clickOn
    
    return None  

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]
# device.shell('input tap 155 1221')

def click(x, y):
    device.shell('input tap %i %i' % (x, y))

def screenshot():
    image = device.screencap()
    fullPath = './img/' + str(time.time()) + '.png' 
    with open(fullPath, 'wb') as f:
        f.write(image)
    return fullPath

path = screenshot()
location = None
match args.type:
    case 'hand':
        location = findImg(path, 'hand-main', HAND_MAIN_MIN, type=HAND_MAIN_TYPE, clickPos='xy')
    case 'btn':
        location = findImg(path, 'green-btn', GREEN_BTN_MIN, type=GREEN_BTN_TYPE, clickPos='center')



if not location == None:
    click(location[0], location[1])
    print("Click on: %i %i" % (location[0], location[1]))

else: print("Not recognized")


os.remove(path)