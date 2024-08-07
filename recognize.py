#!/usr/bin/env python3

import cv2
import numpy as np
import os.path

output_path = './output/'

img_path = './img/btn/'
needle_path = './img/neddle/green-btn.png'
imgBaseName = 'greenbutton'
normalizer = 1 # 200000000

if not os.path.exists(output_path):
    os.makedirs(output_path)

types = [
    # cv2.TM_SQDIFF,
    # cv2.TM_SQDIFF_NORMED,
    # cv2.TM_CCORR,
    cv2.TM_CCORR_NORMED,
    # cv2.TM_CCOEFF,  
    # cv2.TM_CCOEFF_NORMED
]
i = 1
while True:
    path = img_path + imgBaseName + str(i) + ".png"
    if not os.path.exists(path):
        break

    for type in types:
        print = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        needle = cv2.imread(needle_path, cv2.IMREAD_UNCHANGED)
                        
        result = cv2.matchTemplate(print, needle, type)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        needleW = needle.shape[1]
        needleH = needle.shape[0]
        cv2.rectangle(print, max_loc, (max_loc[0]+needleW, max_loc[1]+needleH), (0,255,255), 2)
        # cv2.imwrite(output_path + 'output' + str(i) + '.png', print1)
        cv2.imwrite('%soutput%s-%s-[%s].png' % (output_path, str(i), str(type), str(round(max_val / normalizer, 2))), print)


    i += 1

