#!/bin/bash
echo "Fetching Dependencies for Sheila.py"

#Primary Dependencies
sudo apt-get update
sudo apt-get install python-imaging-tk
sudo apt-get install espeak
pip install pyttsx
pip install SpeechRecognition
pip install weather-api
pip install Pillow
pip install rpi_backlight

#Secondary Dependencies
#sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 libav-tools
sudo apt-get install python-pyaudio
pip install google-api-python-client
pip install monotonic
sudo apt-get install flac

#Will eventually add section to compile 
#OPENCV2 when facial recognition is added again
