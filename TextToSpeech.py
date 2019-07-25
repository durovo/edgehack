import pyttsx3
import threading
from GlobalHelpers import *

def engine_thread():
    engine = pyttsx3.init()
    while True:
        text = global_queue.get(block=True)
        if text == "end":
            break
        engine.say(text)
        engine.runAndWait()

t = threading.Thread(target=engine_thread, daemon=True)
t.start()

def BotSpeak(unique_id, text):
    print("unique_id", unique_id)
    global_queue.put(text)
