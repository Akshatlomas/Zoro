import speech_recognition as sr
import webbrowser 
import time
import os
import random
import subprocess
from rapidfuzz import fuzz
from datetime import datetime
from gpt4all import GPT4All
# used to open app like spotify 
#pip install pocketsphinx
from spotify import play_song

#sr.Recognizer() speech recognition process ko handle karne ke liye ek object banata hai.
recognizer=sr.Recognizer()       
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True    
recognizer.pause_threshold = 1.2   # kitni silence ke baad stop kare
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5
# engine = pyttsx3.init('nsss') # initialize ho jaayega pyttsx engine
# voices = engine.getProperty('voices')
# engine.setProperty('rate', 160)
# engine.setProperty('voice', voices[18].id)  
# engine.setProperty('volume', 1.0)
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
def chat_response(prompt):
    with model.chat_session():
        response = model.generate(
            f"You are Zoro, a smart assistant. Answer clearly: {prompt}",
            max_tokens=100,
            temp=0.7
        )
    return response
def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p")
def speak(text):
  # engine.say(text)
   #engine.runAndWait()
   os.system(f'say -v Daniel "{text}"')
def wake_response():
    responses = [
        "Yes Captain",
        "I'm listening",
        "How can I help",
        "Ready"
    ]
    speak(random.choice(responses))
def ProcessCommand(c):
    if"open google"in c.lower():
        speak("Opening Google")
        time.sleep(0.5)
        webbrowser.open("https://google.com")
    elif "time" in c.lower() or "what's the time" in c.lower() or "what is the time" in c.lower():
        current_time = time.strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif"open brave" in c.lower():
        speak("Opening Brave")
        subprocess.run(["open","-a","Brave Browser"])
    elif"open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com")
    elif"open spotify" in c.lower():
        speak("opening spotify")
        subprocess.run(["open", "-a", "Spotify"])
    elif"play" in c.lower() and "spotify" in c.lower():
        song = c.lower().replace("play", "").replace("on spotify", "").strip()
        response = play_song(song)
        speak(response)
        # Mac system
    elif "volume up" in c:
        os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) + 10)'")
        speak("Increasing volume")
    elif "volume down" in c:
        os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) - 10)'")
        speak("Decreasing volume")
    elif "mute" in c:
        os.system("osascript -e 'set volume output muted true'")
        speak("Muted")
    elif "unmute" in c:
        os.system("osascript -e 'set volume output muted false'")
        speak("Unmuted")
    elif "sleep" in c:
        os.system("pmset sleepnow")
        speak("Sleeping Mac")
    else:
        speak("Thinking...")
        reply = chat_response(c)
        speak(reply)
   
    print(c)
    pass
if __name__=="__main__": 
        speak("Initializing zoro")
        while(True):
            # wait for the wake word zoro
            #obtain audio from mic
            with sr.Microphone() as source:
                recognizer.dynamic_energy_threshold = True
                recognizer.energy_threshold = 250
                recognizer.pause_threshold = 1.0
                recognizer.adjust_for_ambient_noise(source, duration=2)
                speak("Zoro Initialized")

                while True:
                    try:
                        print("Listening for wake word...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                        word = recognizer.recognize_google(audio, language="en-IN")

                        wake_word = "zoro"

                        wake_words = ["zoro", "zor", "zorro", "joro", "guru"]

                        spoken_text = word.lower().split()

                        match = False

                        for w in spoken_text:
                            for wake in wake_words:
                                if fuzz.ratio(w, wake) > 75:
                                    match = True
                                    wake_response()
                                    break

                        if match:
                            
                            print("Listening for command...")
                            audio = recognizer.listen(source, timeout=5, phrase_time_limit=12)
                            command = recognizer.recognize_google(
                                        audio,
                                        language="en-IN",
                                        show_all=False
                                    )

                            ProcessCommand(command)
                       

                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        print("Network error")