#!/usr/bin/env python
"""
Created on Mon Jan  8 18:40:33 2018

@author: Andy Lezcano

This is Sheila's core,this function will call all of the other functions
"""
print("Pre-Compilation starting...")

#Sheila's face recognition imports
#import Face_Recon_Proc as FR

#Sheila's text-to-speech imports
import pyttsx

#Sheila's speech recognition imports
import VIO_Recon_Proc as VO

#Sheila's face-display imports
import Tkinter as tk
from PIL import Image, ImageTk
import rpi_backlight as bl

#Sheila's weather imports
from weather import Weather

#General-use imports
#import multithreading
from datetime import datetime
import time
import sys
import os

def Sheila_Core():  
    try:
        #Local time variables for Sheila
        startTime = time.time()
        seconds = 0
        minutes = 0
        
        #This function initializes the UI
        rootW=setupGUI()
        
        #This function sets the screen to OFF for the initialization
        blAdjust(11)
             
        #This command clears the terminal window for easier reading
        os.system('cls' if os.name == 'nt' else 'clear')

        #Quick message at the start to record start time
        bootTime=datetime.now()
        say("Hello, booting up, the time is " + str(bootTime.hour) + " " + str(bootTime.minute))
        
        #Setup of flags/initialized classes that will be used later
        weather = Weather()
        alarmFlag = True
        detFlag = False
        
        locale = weather.lookup(12588678)
        condition = locale.condition     
        say("The weather is currently " + condition.text + " and it is currently " + condition.temp + " degrees celsius.")
        
        while True:
            
            #This section sets up the alarm clock functionality 
            currentTime = datetime.now().time() 
            if currentTime.hour == 6 and alarmFlag is True:             
                locale = weather.lookup(12588678)
                condition = locale.condition()
                            
                say("Good morning, Andy. It is time to get up and start your day.")
                say("The time is currently " + str(currentTime.hour) + " " + str(currentTime.minute))
                say("The weather is currently " + condition.text() + " and it is currently " + condition.temp() + " degrees celsius.")
                alarmFlag = False
            if currentTime.hour > 6 and alarmFlag is False:
                alarmFlag = True

            #Incrementing the time counter
            seconds = int(time.time() - startTime) - minutes * 60
            if seconds >= 60 :
                minutes += 1
                seconds = 0
                
            #This is the voice input stream
            inputVO = VO.recordAndInterpret()

            #This section handles the VO interpretation
            fullVOSplit = inputVO.split()
            for word in fullVOSplit:
                if word.lower() == "sheila" and detFlag is False:
                    print("--------------------------------------------------")
                    print("...I heard my name...")
                    print("--------------------------------------------------")
                    say("I heard you, you said: " + str(inputVO))
                    detFlag = True
                    break
                elif detFlag is True:
                    pass
                
            #If more than 3 minutes have passed and the detection flag is false
#            if minutes > 3 and detFlag is False:
#                print ("---Attempting Face Detection---")
#                alDet = FR.detFaceNow(False)
#                if alDet is True:
#                    print ("...I voEnginesee you...")
#                    say('I think I see you! Would you like to chat?')
#                    detFlag = True
#                    minutes = 0
#                    seconds = 0
#                    startTime = time.time()  
#            if minutes > 5:
#                minutes = 0
#                seconds = 0
#                startTime = time.time()  
#                detFlag = False
                    
    except KeyboardInterrupt:
        bl.set_brightness(255, smooth=False, duration = 0.1)
        rootW.destroy()
        sys.exit()
       
def blAdjust(brightness):
    bl.set_brightness(brightness, smooth=True, duration = 0.25)

def setupGUI():
    rootW = tk.Tk()       
    rootW.geometry("800x480")
    rootW.configure(background = 'black', highlightbackground='black', borderwidth=0)
    rootW.attributes('-fullscreen', True)

    imgMPath = "Sheila.jpg"        
    imgMain = Image.open(imgMPath)
    imgMain = imgMain.resize((800, 480), Image.ANTIALIAS)
    imgMainPI = ImageTk.PhotoImage(imgMain)
    
    imPanel = tk.Label(rootW, image = imgMainPI, background = 'black', highlightbackground='black', borderwidth=0)
    imPanel.pack(expand=True)
    rootW.update()
    return rootW
        
def say(whatToSay):
    blAdjust(255)
    voEngine = pyttsx.init()
    voEngine.setProperty('voice', 'english+f3')
    voEngine.setProperty('rate', 150)
    voEngine.setProperty('volume', 0.25)
    voEngine.say(whatToSay)
    print("--------------------------------------------------")
    print whatToSay
    print("--------------------------------------------------")
    talkingNOW = voEngine.runAndWait()
    blAdjust(11)

Sheila_Core()