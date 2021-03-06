import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
r = sr.Recognizer()


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry! I didn't get it")
        except sr.RequestError:
            speak("Sorry! the speech service is down")
        return voice_data


def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 9999999)
    audio_file = f'audio-{str(r)}.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if 'what is your name' in voice_data:
        speak("I don't have a name yet")
    if 'what time is it' in voice_data:
        speak(time.ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search?')
        url = f'https://google.com/search?q={search}'
        webbrowser.get().open(url)
        speak(f'Results for {search}')
    if 'location' in voice_data:
        loc = record_audio('What location do you need?')
        url = f'https://google.com/maps/place/{loc}/&amp;'
        webbrowser.get().open(url)
        speak(f'Location of {loc}')
    if 'exit' in voice_data:
        speak('Goodbye')
        exit()



# time.sleep(1)
speak('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)
