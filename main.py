import os
import eel
import subprocess

from engine.features import playAssistantSound

def start():
    eel.init("www")
    playAssistantSound()
    
    # Open Brave in app mode
    subprocess.Popen(['open', '-na', 'Brave Browser', '--args', '--app=http://localhost:8000/index.html'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Start Eel without output
    eel.start('index.html', mode=None, host='localhost', block=True, suppress_warning=True)
start()