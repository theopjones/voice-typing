'''
    Written in 2022 by Theodore Jones tjones2@fastmail.com

    To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.

    You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
'''

import io
from pydub import AudioSegment
import speech_recognition
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
    global last_dictation_time
    print(predicted_text)
    keyboard.type(predicted_text)
    if len(predicted_text) > 3: 
        keyboard.type("\n")
        last_dictation_time = time.time()

def SaveCollectedAudioClipToTempFolder(audio_clip):
    global temporary_folder
    audio_file_path = os.path.join(temporary_folder,"voice_recording_" + str(time.time()) + ".wav")
    audio_clip.export(audio_file_path, format="wav")
    return audio_file_path

def ListenUntilSoundIsHeard(speech_listener):
    global microphone_device
    with microphone_device as dictation_audio_source:
        raw_audio_of_speech = speech_listener.listen(dictation_audio_source, timeout = 30)
        processed_audio_of_speech = io.BytesIO(raw_audio_of_speech.get_wav_data())
        audio_segment_to_be_sent_to_whisper = AudioSegment.from_file(processed_audio_of_speech)
    return audio_segment_to_be_sent_to_whisper

def ListenThenSendAudioToWhisper(sound_recording_queue,speech_listener):
    try:
        path_to_recorded_audio_clip = SaveCollectedAudioClipToTempFolder(ListenUntilSoundIsHeard(speech_listener))
        sound_recording_queue.put_nowait(path_to_recorded_audio_clip)
    except speech_recognition.WaitTimeoutError:
        pass


def MicLoop(speech_listener):
    global DictationOn
    global audio_model
    while True:
        if DictationOn == True: 
         if (int(time.time()) - last_dictation_time) > auto_mic_off_time:
                DictationOn = False
                tray.setIcon(MicOff)
         else:
            ListenThenSendAudioToWhisper(sound_recording_queue,speech_listener)                     

def TrayIconClicked(): 
    global DictationOn
    global last_dictation_time
    global sound_recording_queue
    last_dictation_time = int(time.time())
    if DictationOn == False: 
       DictationOn = True
       tray.setIcon(MicOn)
       sound_recording_queue = queue.SimpleQueue()
    else:  
        DictationOn = False
        tray.setIcon(MicOff)

def ModelLoop():
    audio_model = whisper.load_model(model)
    while True:
        if sound_recording_queue.empty() == False:
            tray.setIcon(robot_face)
            file_save_path = sound_recording_queue.get_nowait()
            result = audio_model.transcribe(file_save_path)
            os.remove(file_save_path) 
            predicted_text = result["text"]
            if DictationOn == True:
                HandleOutputOfDictation(predicted_text)
            if DictationOn == True: 
               tray.setIcon(MicOn)
            if DictationOn == False:
               tray.setIcon(MicOff)     

def OpenConfigFileInEditor():
    subprocess.call(["xdg-open", config_file_path])

#Create Temporary Folder
temporary_folder = tempfile.mkdtemp()

#load config file 
home_folder_path = os.path.expanduser('~')
config_file_path = os.path.join(home_folder_path, "voice_typing_config.txt")

if not os.path.exists(config_file_path):
    shutil.copyfile("sampleconfig.txt", config_file_path)

ConfigFile = configparser.ConfigParser()
ConfigFile.read(config_file_path)

#create background thead for model
model = ConfigFile['ModelAttributes']['model']
english = bool(ConfigFile['ModelAttributes']['english'])

sound_recording_queue = queue.SimpleQueue()
model_thread = threading.Thread(target=ModelLoop)
model_thread.daemon = True
model_thread.start()

#create listener 
microphone_device = speech_recognition.Microphone(sample_rate=44100)
speech_listener = speech_recognition.Recognizer()

speech_listener.energy_threshold = int(ConfigFile['ModelAttributes']['energy'])
speech_listener.dynamic_energy_threshold = bool(ConfigFile['ModelAttributes']['dynamic_energy'])
speech_listener.pause_threshold = float(ConfigFile['ModelAttributes']['pause'])
auto_mic_off_time = int(ConfigFile['VoiceTypingAttributes']['auto_mic_off_time'])

#Create background thread for microphone listener 
thread = threading.Thread(target=MicLoop,args=(speech_listener,) )
thread.daemon = True
thread.start()

#keyboard control 
keyboard = Controller()

#time since last dictation
last_dictation_time = int(time.time())

app = QApplication([])
app.setQuitOnLastWindowClosed(False)        

#load icons
MicOff = QIcon("1F507_color.png")
MicOn = QIcon("1F3A4_color.png")
robot_face = QIcon("1F916_color.png")

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