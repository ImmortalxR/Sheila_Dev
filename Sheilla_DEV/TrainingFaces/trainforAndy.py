#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 21:02:33 2018

@author: Andy Lezcano
"""

import picamera
import time

num = 1

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.rotation = 270
camera.start_preview()

while num < 1000:
        nameString = str(num) + "_Andy_Test.jpg"
        camera.capture(nameString)
        num = num + 1
        time.sleep(0.01)