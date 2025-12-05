import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"Bot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens to the microphone and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            text = r.recognize_google(audio)
            print(f"User: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
