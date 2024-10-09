import re
import struct
import time
import logging
import pvporcupine
import pyaudio
import pyautogui as autogui


HOTWORDS = ["computer"]  # Define your hotwords here

def extract_yt_term(command: str) -> str:
    """Extract the term for YouTube search from the command."""
    pattern = r'play\s+(.*?)\s+(on\s+youtube|youtube)'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    """Remove specific words from a string."""
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    return ' '.join(filtered_words)

def hotword():
    """Listen for the hotword and trigger an action."""
    porcupine = None
    paud = None
    audio_stream = None

    try:
        # Pass the access_key while creating the Porcupine instance
        porcupine = pvporcupine.create(access_key="h/8R+eYBat5SQaIIx74RS58hQ2g3mfWs47XGuWxs6zOUorTUg6EVCg==", keywords=["computer"])

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
            input_device_index=0  # Adjust index if needed
        )

        logging.info("Listening for hotword...")

        while True:
            data = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, data)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                logging.info(f"Hotword detected!")
                start_application()  # Call your main application

    except Exception as e:
        logging.error(f"Error in hotword detection: {e}")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def start_application():
    """Function to start your application."""
    logging.info("Starting application...")
    from main import start  # Import inside function to avoid circular import issues
    start()

if __name__ == "__main__":
    try:
        hotword()
    except KeyboardInterrupt:
        logging.info("Exiting gracefully...")
