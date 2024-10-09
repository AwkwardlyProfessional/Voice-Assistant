import multiprocessing
import logging
import time  # Import time for delay

# Configure logging
logging.basicConfig(level=logging.INFO)
#acess key
access_key = "u9+OTpu9A5ZB+JHuxIzWLTDJHSZ6FMytsk4e88aK1XM4Pb+rzpqa7w=="  # Define your access key here

# To run the computer assistant
def start_Computer():
    """Start the computer assistant."""
    try:
        logging.info("Process 1 (computer) is running.")
        from main import start
        start()
  # Ensure that the `start` function in main.py runs without issues
    except Exception as e:
        logging.error(f"Error in computer process: {e}")

# To run hotword detection
def listen_hotword(access_key):
    """Listen for the hotword."""
    try:
        logging.info("Process 2 (Hotword Listener) is running.")
        from engine.features import hotword
        hotword(access_key)  # Pass the access_key as an argument
    except Exception as e:
        logging.error(f"Error in Hotword process: {e}")

# Start both processes
if __name__ == '__main__':

    p2 = multiprocessing.Process(target=listen_hotword, args=(access_key,))
    p2.start()



    # Allow a small delay to ensure the hotword listener is ready
    time.sleep(1)

    p1 = multiprocessing.Process(target=start_Computer)  # Then start the computer assistant
    p1.start()


    # Wait for the computer process to finish
    p1.join()

    # If the hotword listener is still alive, terminate it
    if p2.is_alive():
        logging.info("Terminating hotword listener.")
        p2.terminate()
        p2.join()

    logging.info("System stopped.")
