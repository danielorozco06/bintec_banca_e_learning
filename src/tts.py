"""
Text to speech module
"""

from gtts import gTTS
import os

gTTS(text="Buenos días", lang="es").save("audios/good.mp3")
os.system("mpg123 audios/good.mp3 &")
