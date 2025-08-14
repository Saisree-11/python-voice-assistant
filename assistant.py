import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import psutil
import wikipedia
import smtplib
import atexit
import warnings
import sys

# ----------------- Suppress Warnings -----------------
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ----------------- Initialize Speech Engine -----------------
engine = pyttsx3.init()

# Ensure pyttsx3 stops cleanly on exit
def cleanup():
    try:
        engine.stop()
    except Exception:
        pass

atexit.register(cleanup)

# ----------------- Speak Function -----------------
def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ----------------- Listen Function -----------------
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        engine.say(f"You said: {query}")
        engine.runAndWait()
    except sr.UnknownValueError:
        talk("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        talk("Speech service is down.")
        return ""
    except Exception:
        talk("Something went wrong while processing your voice.")
        return ""

    return query.lower()

# ----------------- Email Function -----------------
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Use App Password for Gmail instead of your real password
        server.login("your-email@gmail.com", "your-app-password")
        server.sendmail("your-email@gmail.com", to, content)
        server.quit()
    except Exception as e:
        talk(f"Error sending email: {e}")

# ----------------- Main Assistant -----------------
def run_sai():
    talk("Hey Sai Sree, I am your assistant. How can I help you today?")
    while True:
        command = take_command()

        if not command:
            continue

        # Exit
        if any(word in command for word in ["exit", "quit", "stop"]):
            talk("Okay, see you later. Goodbye!")
            cleanup()
            sys.exit(0)

        # Websites
        elif "open youtube" in command:
            talk("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in command:
            talk("Opening Google")
            webbrowser.open("https://google.com")

        elif "open whatsapp" in command:
            talk("Opening WhatsApp Web")
            webbrowser.open("https://web.whatsapp.com")

        # Applications
        elif "open notepad" in command:
            talk("Opening Notepad")
            os.system("notepad")

        elif "open calculator" in command:
            talk("Opening Calculator")
            os.system("calc")

        elif "open cmd" in command:
            talk("Opening Command Prompt")
            os.system("start cmd")

        # Battery
        elif "battery" in command:
            battery = psutil.sensors_battery()
            talk(f"Battery is at {battery.percent} percent")
            if battery.power_plugged:
                talk("Laptop is charging")

        # Date & Time
        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            talk(f"Current time is {time}")

        elif "date" in command:
            date = datetime.datetime.now().strftime("%B %d, %Y")
            talk(f"Today's date is {date}")

        # Wikipedia
        elif "who is" in command or "what is" in command:
            topic = command.replace("who is", "").replace("what is", "").strip()
            try:
                info = wikipedia.summary(topic, sentences=2)
                talk(info)
            except:
                talk("Sorry, I couldn't find information on that.")

        # Notes
        elif "make a note" in command:
            talk("What should I write?")
            note = take_command()
            if note:
                with open("note.txt", "a") as f:
                    f.write(note + "\n")
                talk("Note added.")

        # Email
        elif "send email" in command:
            talk("What should I say?")
            content = take_command()
            send_email("recipient-email@gmail.com", content)
            talk("Email has been sent.")

        # Joke
        elif "joke" in command:
            talk("Why don’t skeletons fight each other? They don’t have the guts.")

        else:
            talk("I don't know that yet, but I'm learning.")

# ----------------- Run Assistant -----------------
if __name__ == "__main__":
    run_sai()
