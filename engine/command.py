import pyttsx3
import speech_recognition as sr
import eel

# Initialize the voice engine globally
engine = None

def init_voice():
    """Initialize the text-to-speech engine and set voice properties."""
    global engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Set the voice to "Samantha" if available
    for voice in voices:
        if "Samantha" in voice.name:
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 174)  # Set speaking rate

def speak(text):
    """Speak the given text and update the UI."""
    global engine
    eel.DisplayMessage(text)  # Display text on UI
    if engine:
        engine.say(text)  # Speak the text
        engine.runAndWait()  # Wait for completion

def takeCommand(phrase_time_limit=6):
    """Listen for a command from the microphone and return it as text."""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            eel.DisplayMessage('Listening timed out...')
            return ""
        except Exception as e:
            eel.DisplayMessage(f"Error during listening: {str(e)}")
            return ""

    try:
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        eel.DisplayMessage(f'User said: {query}')
        return query.lower()
    except sr.UnknownValueError:
        eel.DisplayMessage("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        eel.DisplayMessage(f"Google Speech Recognition error: {str(e)}")
        return ""
    except Exception as e:
        eel.DisplayMessage(f"Error: {str(e)}")
        return ""

@eel.expose
def allCommands(phrase_time_limit=6):
    """Handle user commands based on the recognized speech."""
    try:
        query = takeCommand(phrase_time_limit)
        if query:
            if "open" in query:
                app_name = query.split("open", 1)[1].strip()
                if app_name:
                    from engine.features import openCommand
                    eel.DisplayMessage(f"Opening {app_name}...")
                    openCommand(app_name)  # Adjust as needed for your platform
                else:
                    eel.DisplayMessage("No application name provided.")
            elif "on youtube" in query:
                from engine.features import PlayYoutube
                PlayYoutube(query)
            else:
                eel.DisplayMessage("Command not recognized.")
        else:
            eel.DisplayMessage("No command recognized.")
    except Exception as e:
        eel.DisplayMessage(f"Error: {str(e)}")
    
    eel.ShowHood()  # Update the UI after executing the command

# Initialize the voice engine when the script starts
init_voice()
