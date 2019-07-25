import pyttsx3
import threading
from GlobalHelpers import *
import time
from collections import defaultdict

message_interval = 5

message_timestamp_dict = defaultdict(lambda: -1)

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
    ctime = time.time()
    mtime = message_timestamp_dict[unique_id]
    if ctime - mtime > message_interval or mtime == -1:
        message_timestamp_dict[unique_id] = time.time()
        print("speaking message ")
        global_queue.put(text)
    