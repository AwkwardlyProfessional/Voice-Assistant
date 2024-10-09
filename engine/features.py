import logging
import os
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui as autogui
import pywhatkit as kit
import pvporcupine
from engine.command import speak
from engine.configure import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words

# Constants
MUSIC_DIR = "www/assests/audio/start_sound.mp3"
HOTWORDS = ["computer"]

@eel.expose
def playAssistantSound():
    """Play the assistant start sound."""
    playsound(MUSIC_DIR)

def openCommand(query):
    """Open an application or website based on user command."""
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()
    app_name = query.strip()

    if not app_name:
        speak("Application not found.")
        return

    with sqlite3.connect("computer.db") as conn:
        cursor = conn.cursor()
        try:
            print(f"Trying to open: {app_name}")  # Debugging output
            
            # Check for applications first
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()
            print(f"App query results: {results}")  # Debugging output
            
            if results:
                speak(f"Opening {app_name}")
                os.system(f'open -a "{results[0][0]}"')
            else:
                # Check for websites next
                cursor.execute('SELECT url FROM websites WHERE name = ?', (app_name,))
                results = cursor.fetchall()
                print(f"Website query results: {results}")  # Debugging output

                if results:
                    speak(f"Opening {app_name} website in a new window...")
                    webbrowser.open_new(results[0][0])
                else:
                    speak(f"Opening {app_name}...")
                    try:
                        os.system(f'open -a "{app_name.capitalize()}"')
                    except Exception as e:
                        speak(f"Failed to open {app_name}. Error: {e}")
        except sqlite3.Error as db_error:
            speak(f"Database error: {db_error}")
            print(f"Database error: {db_error}")  # Debugging output
        except Exception as e:
            speak(f"Something went wrong: {e}")

def PlayYoutube(query):
    """Play a YouTube video based on the command."""
    search_term = extract_yt_term(query)
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        try:
            kit.playonyt(search_term)
        except Exception as e:
            speak(f"Could not play the video. Error: {e}")
    else:
        speak("Could not extract the YouTube search term.")

HOTWORDS = ["computer"]  # Define your hotwords here
def hotword(access_key):
    """Continuously listen for the hotword and trigger actions."""
    porcupine = None
    paud = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key=access_key, keywords=HOTWORDS
        )
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        logging.info("Listening for hotword...")

        # Keep listening for the hotword indefinitely
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm_unpacked)

            if keyword_index >= 0:
                logging.info("Hotword detected!")
                trigger_command()  # Function to trigger the required action

    except Exception as e:
        logging.error(f"Error in hotword detection: {str(e)}")

    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()


def trigger_command():
    """Trigger the specific command on hotword detection."""
    # Using hotkey to simulate Control + Shift + J
    autogui.hotkey('ctrl', 'shift', 'j')
    logging.info("Control + Shift + J executed.")
