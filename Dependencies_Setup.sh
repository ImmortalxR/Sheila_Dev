#!/bin/bash
echo "Fetching Dependencies for Sheila.py"

#Primary Dependencies
pip install pyttsx
pip install SpeechRecognition
pip install weather-api
pip install Pillow

#Secondary Dependencies
sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools
pip install pyaudio
pip install google-api-python-client
pip install monotonic

#Will eventually add section to compile 
#OPENCV2 when facial recognition is added again
