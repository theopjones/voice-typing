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

import threading

from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import QThread

from pynput.keyboard import Key, Controller

#Set Global Values
DictationOn = False

def HandleOutputOfDictation(predicted_text):
    global keyboard
    keyboard.type(predicted_text)

def DictationLoop():
    global DictationOn
    global audio_model
    #Set Config Values
    english = True
    energy = 300
    dynamic_energy = False
    pause = 0.8

    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, "temp.wav")

    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy
    print("Starting Dictation Loop")   
    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        while DictationOn == True:
            #get and save audio to wav file
            audio = r.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav")

            result = audio_model.transcribe(save_path)
            predicted_text = result["text"]
            if DictationOn == True:
                HandleOutputOfDictation(predicted_text)
    print("Dictation Loop Stopped")                      

def TrayIconClicked(): 
    global DictationOn
    if DictationOn == False: 
       DictationOn = True
       thread = threading.Thread(target=DictationLoop)
       thread.daemon = True
       thread.start()
       tray.setIcon(MicOn)
    else:  
        DictationOn = False
        tray.setIcon(MicOff)

#load model
model = "medium"
audio_model = whisper.load_model(model)

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
  
# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)
  
app.exec_()