import random
import queue
import os
import pandas as pd
import json
botqueue_queue = queue.Queue()
botlistening = False
accuracy_queue = queue.Queue()
global_queue = queue.Queue()

class GlobalState():
    def __init__(self):
        self.continue_training = True
        self.rep_count = 0
        self.stopped = False
        self.squats = pd.DataFrame(columns=['name', 'reps'])
        self.pushups = pd.DataFrame(columns=['name', 'reps'])
        self.bicepcurls = pd.DataFrame(columns=['name', 'reps'])
        self.squats_csv = 'squats.csv'
        self.pushups_csv = 'pushups.csv'
        self.bicepcurls_csv = 'bicepcurls.csv'
        self.exercise = ""
        if os.path.exists(self.squats_csv):
            self.squats = pd.read_csv(self.squats_csv)
        if os.path.exists(self.pushups_csv):
            self.pushups = pd.read_csv(self.pushups_csv)
        if os.path.exists(self.bicepcurls_csv):
            self.bicepcurls = pd.read_csv(self.bicepcurls_csv)
    def save_leaderboard(self):
        self.squats.to_csv(self.squats_csv)
        self.pushups.to_csv(self.pushups_csv)
        self.bicepcurls.to_csv(self.bicepcurls_csv)
    def get_leaderboard(self):
        self.squats = self.squats.sort_values(by=['reps'], ascending=False)
        self.pushups = self.pushups.sort_values(by=['reps'], ascending=False)
        self.bicepcurls = self.bicepcurls.sort_values(by=['reps'], ascending=False)
        return {'squats': json.loads(self.squats.to_json(orient='values')), 'pushups': json.loads(self.pushups.to_json(orient='values')), 'bicepcurls': json.loads(self.bicepcurls.to_json(orient='values'))}
    
    def update_leaderboard(self):
        if self.exercise == "squats":
            self.squats = self.squats.append({'name': self.name, 'reps':self.rep_count}, ignore_index=True)
            
        elif self.exercise == "pushups":
            self.pushups = self.pushups.append({'name': self.name, 'reps':self.rep_count}, ignore_index=True)
        else:
            print('biceps')
            self.bicepcurls = self.bicepcurls.append({'name': self.name, 'reps':self.rep_count}, ignore_index=True)
            print(self.bicepcurls)

        
global_state = GlobalState()
botAnswers = {
    "greeting":["Hi, I am your digital smart trainer. What is your name?"],
    "exerciseQuestion":"Hey {} , would you like to do plank.",
    "positiveSentiment":["Great, get in the position for plank and we will start in."],
    "negativeSentiment":["Sorry to know that. Well, Have a nice day."],
    "saysomething":["Sorry, I didn't get you. Please repeat."],
    "quit":["Sorry, something bad occured. I am quitting."],
    "funnyRepeat":["Talk less and work hard in the gym. Please repeat again."]
}


def getRandomBotAnswers(arr):
    rand_idx = random.randrange(len(arr))
    return arr[rand_idx]