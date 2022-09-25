'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.    

    This file contains modified code from https://github.com/mallorbc/whisper_mic
'''

import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import subprocess, sys
from subprocess import call
import time

import configparser
import shutil

import threading
import queue

from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import QThread

from pynput.keyboard import Key, Controller

#Set Global Values
DictationOn = False

def HandleOutputOfDictation(predicted_text):
    global keyboard
    print(predicted_text)
    keyboard.type(predicted_text)
    if len(predicted_text) > 10: 
        keyboard.type("\n")

def DictationLoop():
    global DictationOn
    global audio_model
    temp_dir = tempfile.mkdtemp()

    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy
    print("Starting Dictation Loop")   
    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        while True:
            if DictationOn == True: 
             #get and save audio to wav file
             print("Recording Audio")
             save_path = os.path.join(temp_dir, str(time.time()) + "temp.wav")
             audio = r.listen(source)
             data = io.BytesIO(audio.get_wav_data())
             audio_clip = AudioSegment.from_file(data)
             audio_clip.export(save_path, format="wav")
             print("Recorded Sound Clip")
             print(DictationOn)
             sound_recording_queue.put_nowait(save_path)
    print("Dictation Loop Stopped")                      

def TrayIconClicked(): 
    global DictationOn
    if DictationOn == False: 
       DictationOn = True
       tray.setIcon(MicOn)
    else:  
        DictationOn = False
        tray.setIcon(MicOff)

def ModelLoop():
    audio_model = whisper.load_model(model)
    print("Model Active")
    while True:
        if sound_recording_queue.empty() == False:
            file_save_path = sound_recording_queue.get_nowait()
            result = audio_model.transcribe(file_save_path)
            os.remove(file_save_path) 
            predicted_text = result["text"]
            if DictationOn == True:
                HandleOutputOfDictation(predicted_text)

def OpenConfigFileInEditor():
    subprocess.call(["xdg-open", config_file_path])

#load config file 
home_folder_path = os.path.expanduser('~')
config_file_path = os.path.join(home_folder_path, "voice_typing_config.txt")

if not os.path.exists(config_file_path):
    shutil.copyfile("sampleconfig.txt", config_file_path)

ConfigFile = configparser.ConfigParser()
ConfigFile.read(config_file_path)

model = ConfigFile['ModelAttributes']['model']
english = bool(ConfigFile['ModelAttributes']['english'])
energy = int(ConfigFile['ModelAttributes']['energy'])
dynamic_energy = bool(ConfigFile['ModelAttributes']['dynamic_energy'])
pause = float(ConfigFile['ModelAttributes']['pause'])

#create background thead for model
sound_recording_queue = queue.SimpleQueue()
model_thread = threading.Thread(target=ModelLoop)
model_thread.daemon = True
model_thread.start()

#Create background thread for microphone listener 
thread = threading.Thread(target=DictationLoop)
thread.daemon = True
thread.start()

#keyboard control 
keyboard = Controller()

app = QApplication([])
app.setQuitOnLastWindowClosed(False)        

#load icons
MicOff = QIcon("1F507_color.png")
MicOn = QIcon("1F3A4_color.png")

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(MicOff)
tray.setVisible(True)
tray.activated.connect(TrayIconClicked)

# Creating the menu 
menu = QMenu()
  
# Quit Menu Item
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Settings Menu Item
settingsmenu = QAction("Settings")
settingsmenu.triggered.connect(OpenConfigFileInEditor)
menu.addAction(settingsmenu)

# Adding options to the System Tray
tray.setContextMenu(menu)
  
app.exec_()