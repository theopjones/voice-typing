This program provides voice typing on Linux based systems. It records audio from the user's device in real time, and uses the [Whisper library](https://github.com/openai/whisper) to transcribe it to text. It then simulates a keyboard to use this dictated text as an input method. When loaded this tool creates an icon in the system tray that allows activation and deactivation of the speech to text conversion. In the creation of this tool, I have used code from [whisper_mic](https://github.com/mallorbc/whisper_mic). The microphone icon used in the system tray is based on an [icon from the OpenMoji project](https://openmoji.org/library/emoji-1F3A4/). 

I am not affiliated with the developers of Whisper or any of the other upstream libraries used in the creation of this program.
 
It currently defaults to the small quality model, this is configurable by editing the configuration file.  

**Installation of Dependencies**

Using this tool requires first installing Whisper. It is recommended that you confirm that Whisper is fully working before trying this program. 

PyQt5 is also a dependency, it can be installed from the package manager on most linux distros. 

Other dependencies are in the requirements.txt file, and can be installed with `pip install -r requirements.txt`

**Usage** 

 Currently, there is not a separate installer for this program. Therefore, you'll have to start it in the command line by opening the voice-typing.py file with Python 3.
  
 Once open, this program will create a new system tray icon. 
 
 When the microphone is not recording audio for transcription, which is the default configuration for a newly started version of the program, the system tray icon will be a picture of a microphone with a red background.
  
 This icon should look like the following 
 
 ![Microphone with red background](1F507_color.png)
 
 If you click on that icon, the icon will turn green and the microphone will begin to record audio.
 
 ![Green Microphone Icon](1F3A4_color.png)
 
 Once you speak into the microphone, the program will recognize that you are speaking into it. It will then send the audio you're recording to Whisper once the program has detected a sufficiently long pause in your speaking. This pause defaults to 1.5 seconds, although this is configurable in the config file. Recording and pause detection is done using the [speech_recognition](https://pypi.org/project/SpeechRecognition/) library.
 
 When Whisper is processing the recorded audio, the icon changes to a picture of a robot face.
 
 ![Robot Face](1F916_color.png)
   
 Once Whisper has finished transcribing the audio, the program will then simulate a keyboard and type the resulted transcribed text into the currently open and selected text input.It is recommended that when dictating into the program you have a text input with a method of some kind opened and selected. For the typing simulation to work, you will have to have the dialog box selected as if you were about to type into it with your keyboard.
 
 If it is your first time using the program with a given model, the model will be downloaded first before Whisper can transcribe any of the audio collected.Therefore, recorded audio will remain in the queue until this downloading process has been completed. You can check the output in the terminal to determine the status of this downloading process.
   
Since the program is sending the recorded audio to Whisper and also because the audio recording does not stop until the program has detected enough of a pause there will be a delay between when you finish talking and when the text is typed.  The delay is determined by the exact configuration parameters you have used in the config file and also by the dictation quality you have selected by choosing the model.  The delay is also determined by the performance capabilities of the computer you are using. If it is too slow, it is recommended that you choose a lighter weight model, although this comes at the expense of dictation quality.

Dictation will automatically shut off after about 60 seconds of inactivity. This is a configurable setting. 
 
 A video of usage of the program can be found here [https://peertube.theopjones.blog/w/6x5yS96TNnTTdrf11Vwhuh](https://peertube.theopjones.blog/w/6x5yS96TNnTTdrf11Vwhuh) 
 
**Configuration**

On first run, the program creates a file named `voice_typing_config.txt ` in the home folder of the current user. The filename and the path has been chosen for ease of development of the program, and will likely be changed in later revisions. 

Of note are the following two configuration options. 

`model`  This configuration option selects which model to use. The models vary by file size and performance required in the computer being used. The model options are the same as in Whisper. 

`energy`  This configuration option selects the threshold of audio volume required for the program to determine that speech is ongoing and therefore to send recorded audio to whisper. Higher values mean a higher threshold for volume. Setting this parameter too low means that the program will sometimes detect speech ongoing when there is not speech ongoing. The effect of this will be to send empty audio files to Whisper for transcription. Whisper may detect phantom audio in these files and therefore generate text that does not correspond to anything spoken into the program.

`auto_mic_off_time`   This configuration option sets how long the program will wait to shut off the microphone due to inactivity.
 

   



 
  
  