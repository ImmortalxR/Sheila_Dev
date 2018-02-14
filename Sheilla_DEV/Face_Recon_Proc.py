#!/usr/bin/env python
"""
Created on Mon Jan  8 20:48:46 2018

@author: Andy Lezcano

This is Sheila's facial recognition proc, she will use the functions here to do an initial training run to create
the list of faces that she will recognize. She will also use the detFaceNow function often to attempt to detect faces
in her view.
"""

#Import needed modules
import cv2
import os
import numpy as np
import sys
from picamera import PiCamera
import time
from picamera.array import PiRGBArray

#This list contains the names of the known subjects, in the order that they are organized in the TrainingFaces directory
subjects = ["Andy Lezcano"]

#Function to detect a face using OpenCV
def detect_face(img):
    
	#Check if image is already grayscale, if not convert it, and if the image has an invalid number of color channels, exit
    gsCheck = len(img.shape)    
    if gsCheck > 2:
        #Convert the test image to a grayscale image, since opencv face detection expects grayscale images
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif gsCheck == 2:
        grayImg = img
    elif gsCheck < 2:
        sys.exit()

    #Load the OpenCV face detector, in this case I am using LBP frontal face recognition
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')

    #This is the multiscale function that detects faces within the image
    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.2, minNeighbors=5);
    
    #if no faces are detected then I return none for the labels and image
    if (len(faces) == 0):
        return None, None
    
    #Assuming there will only be one face, we extract just the first set of data in faces
    (x, y, w, h) = faces[0]
    
    #Return only the face part of the image
    return grayImg[y:y+w, x:x+h], faces[0]

#This function will read all of the training images, detect the faces from each image
#and will return two lists of exactly same size, one list of faces and another list of labels for each face
def prepare_training_data(data_folder_path):
    
    #Get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)
    
    #Lists, one to hold all subject faces, another to hold all labels
    faces = []
    labels = []
    
    #Go through each directory, and read images within it
    for dir_name in dirs:
        
        #our subject directories start with letter 'S' so ignore any non-relevant directories if any
        if not dir_name.startswith("S"):
            continue;
            
        #Extract label number of subject from dir_name
        label = int(dir_name.replace("S", ""))
        
        #Build path of directory containing images for current subject
        subject_dir_path = data_folder_path + "/" + dir_name
        
        #Get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)
        
        #Go through each image name, read image, detect face and add face to list of faces
        for image_name in subject_images_names:
            
            #Ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;
            
            #Build image path
            image_path = subject_dir_path + "/" + image_name

            #Read image
            image = cv2.imread(image_path)
            
            #Display an image window to show the image, this is commented out in the non-debug version of this script
            #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
            #cv2.waitKey(10)
                        
            #Detect face
            face, rect = detect_face(image)
            
            #Ignore faces that are not detected in training set
            if face is not None:
                #Add face to list of faces
                faces.append(face)
                #Add label for this face
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels

#This will prepare our training data during the initialization of Sheila, this should only have to occur once
print("Preparing FID data...")
faces, labels = prepare_training_data("TrainingFaces")
print("Data prepared...")

#Create the LBPH face recognizer 
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

#Train the face recognizer with our training faces
face_recognizer.train(faces, np.array(labels))

#Function to draw rectangle on image according to given (x, y) coordinates and given width and height
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
#Function to draw text on give image starting from passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

#This function recognizes the person in image passed and draws a rectangle around 
#detected face including the subject name
def predict(test_img):
    #Make a copy of the image, since we don't want to change original image
    img = test_img.copy()
    #Detect a face in the image
    face, rect = detect_face(img)

	#Check to see if no face is found
    if face is None:
        return False

    #If a face is found, attempt to predict the face in the image using our face recognizer 
    label, confidence = face_recognizer.predict(face)
    #Get name of respective label returned by face recognizer
    label_text = subjects[label]
    
    #Draw a rectangle around face detected
    draw_rectangle(img, rect)
    #Draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1]-5)
    
    return img

#This is the workhorse function that will initialize the pi camera, as well as run all of the subroutines
#that will perform the work to identify the faces in the camera images
def detFaceNow(debug):
	#Run this block if debugging is disabled
	if debug is False:
		camera = PiCamera()
		rawCapture = PiRGBArray(camera)   
		camera.resolution = (320, 240)
		camera.rotation = 90
		camera.brightness = 55
		camera.contrast = 1
		time.sleep(2)
				
		rawCapture.truncate(0)
		
		predicted_img = False
		
		camera.capture(rawCapture, format="bgr")
		image = rawCapture.array

		camera.close()

		#perform a prediction
		predicted_img = predict(image)

		if predicted_img is not False:
			return True
		
		return False
	#Run this block if debugging is enabled
	elif debug is True:
		print("Trying to find you...")
		camera = PiCamera()
		rawCapture = PiRGBArray(camera)   
		camera.resolution = (320, 240)
		camera.rotation = 270
		camera.brightness = 55
		camera.contrast = 1
		time.sleep(2)
				
		rawCapture.truncate(0)
		
		predicted_img = False
		
		camera.capture(rawCapture, format="bgr")
		image = rawCapture.array

		camera.close()

		cv2.imshow("image", image)
		cv2.waitKey(1)

		#perform a prediction
		predicted_img = predict(image)

		if predicted_img is not False:
			print ("Andy found...!")
			return True
		
		return False
