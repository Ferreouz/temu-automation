#!/usr/bin/env python3

from ppadb.client import Client
import os.path
import time
import argparse

parser = argparse.ArgumentParser("snap.py")
parser.add_argument("counter", help="Amount of snapshots to take.", type=int)
args = parser.parse_args()

folder = "./"

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]
# device.shell('input tap 155 1221')

imgCount = args.counter
while imgCount > 0:
    imgCount -= 1

    image = device.screencap()
    exists = True
    i = 1
    imgName = folder + "img/print"
    while exists:
        fullPath = imgName + str(i) + ".png"
        i += 1
        if not os.path.exists(fullPath):
            exists = False
            with open(fullPath, 'wb') as f:
                f.write(image)
    time.sleep(0.24)