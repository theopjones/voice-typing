This program provides voice typing on Linux based systems. It records audio from the user's device in real time, and uses the [Whisper library](https://github.com/openai/whisper) to transcribe it to text. 

It then simulates a keyboard to use this dictated text as an input method. When loaded this tool creates an icon in the system tray that allows activation and deactivation of the speech to text conversion. 

Using this tool requires first installing Whisper. 

PyQt5 is also a dependency, it can be installed from the package manager on most distros. Other dependencies are in the requirements.txt file, and can be installed with `pip install -r requirements.txt`

In the creation of this tool, I have used code from [whisper_mic](https://github.com/mallorbc/whisper_mic). The microphone icon used in the system tray is based on an [icon from the OpenMoji project](https://openmoji.org/library/emoji-1F3A4/). 