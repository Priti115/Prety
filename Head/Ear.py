import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore, Style, init
import time
import sys

# Initialize colorama so terminal colors work on all OS
init(autoreset=True)

# Function: Animated "I am listening..." display
def print_loop(listening_flag):
    """
    Displays animated 'I am listening...' text while listening_flag is True.
    """
    while listening_flag[0]:
        for dots in ["", ".", "..", "...", "...."]:
            print(Fore.LIGHTGREEN_EX + f"\r🎤 I am listening{dots} ", end="", flush=True)
            time.sleep(0.3)
    print(Style.RESET_ALL, end="", flush=True)

# Function: Translate Hindi text to English
def Trans_hindi_to_english(txt):
    """
    Translates Hindi text to English using mtranslate.
    Returns English text if successful, otherwise original text.
    """
    try:
        english_text = translate(txt, "en", "hi")
        return english_text
    except:
        return txt

# Function: Detect if text contains Hindi characters
def is_hindi(text):
    """
    Checks if the given text contains Hindi characters
    (Unicode range: \u0900 - \u097F).
    """
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return True
    return False

# Function: Listen once from microphone and return recognized text
def listen():
    """
    Listens to the microphone **once**, processes the recognized speech,
    translates if in Hindi, and prints the result.
    """
    recognizer = sr.Recognizer()

    # Recognition sensitivity parameters
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 4000  # Lower threshold to catch more speech
    recognizer.pause_threshold = 1.2    # Allow longer pauses
    recognizer.phrase_time_limit = 15   # Max duration to capture
    recognizer.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        # Adjust for background noise
        recognizer.adjust_for_ambient_noise(source)
        print(Fore.YELLOW + "Microphone ready!")

        listening_flag = [True]
        anim_thread = threading.Thread(target=print_loop, args=(listening_flag,))
        anim_thread.start()

        try:
            # Listen once (no while loop, so it won’t repeat)
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
            listening_flag[0] = False
            anim_thread.join()

            try:
                # Recognize using Google Speech Recognition (Hindi language)
                recognized_txt = recognizer.recognize_google(audio, language="hi-IN").strip()
            except sr.UnknownValueError:
                recognized_txt = ""
            except sr.RequestError as e:
                recognized_txt = ""
                print(Fore.RED + f"\nAPI Error: {e}")

            # If something is recognized
            if recognized_txt:
                if is_hindi(recognized_txt):
                    translated_txt = Trans_hindi_to_english(recognized_txt)
                    print(Fore.BLUE + f"\rPriti : {translated_txt}")
                else:
                    print(Fore.BLUE + f"\rPriti : {recognized_txt}")
            else:
                print(Fore.RED + "No speech detected.")

        except KeyboardInterrupt:
            listening_flag[0] = False
            anim_thread.join()
            print(Fore.RED + "\nStopping...")

# Start listening (only once)
listen()
