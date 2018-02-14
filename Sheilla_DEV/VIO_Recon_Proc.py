#!/usr/bin/env python
"""
Created on Sat Jan 13 15:26:02 2018

@author: Andy Lezcano

This is Sheila's voice recognition system
"""

import speech_recognition as sr

def recordAndInterpret():
    rec = sr.Recognizer()
    while True:       
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            
        try:
            return rec.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry I do not understand"