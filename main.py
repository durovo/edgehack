from flask import Flask, render_template, redirect, url_for, request,jsonify
from flask_socketio import SocketIO,emit
from demo_utils import start_bicepcurl, start_pushups, start_squats
from GlobalHelpers import global_state
# from GymTrainerBot import *
import demo
from threading import Thread
# import mayank
# import threading
# from GlobalHelpers import accuracy_queue




app = Flask(__name__)
socketio = SocketIO(app)

exercise_thread = 0
# import demo
# import mayank
# demo = None
# def queueMessageEmit():
#     while True:
#         text = accuracy_queue.get(block=True)
#         socketio.emit("pysend", {"data": text})

# @socketio.on('connect')
# def handle_connection():
#     socketio.start_background_task(target=queueMessageEmit)

# def sendPySend():
#     while True:
#         text = accuracy_queue.get(blo
# @socketio.on('uisend')
# def handle_my_custom_event(json):
#     print('received call from UI: ' + str(json))
#     emit("pysend",{"data":"I am Python calling to UI"})


@app.route("/")
def home():
    return render_template("template.html")

@app.route("/bicepcurls")
def start_bicepcurls_async():
    start_exercise_async(start_bicepcurl)

@app.route("/pushups")
def start_pushups_async():
    start_exercise_async(start_squats)

@app.route("/squats")
def start_squats_async():
    start_exercise_async(start_pushups)

@app.route("/stop")
def stop_exercise():
    global_state.continue_training = False
    while not global_state.stopped:
        a = 1
    global_state.stopped = False
    global_state.continue_training = True
    print("The rep count is ", global_state.rep_count)
    return jsonify(rep_count = global_state.rep_count)

def start_exercise_async(excercise_function):
    exercise_thread = Thread(target = excercise_function)
    exercise_thread.daemon = True
    exercise_thread.start()

# @app.route("/bot")
# def startTrainerBot():
#     startBot()
#     return "nothing just run bot"

# @app.route("/botintro")
# def startTrainerBotIntro():
#     greet = startBotGreeting()
#     return jsonify(buttonName = "Your Name?",botanswers=greet)

# @app.route("/humanIntro")
# def startTrainerHumanIntro():
#     greet = humanIntroduction()
#     return jsonify(buttonName = "Hey there!",botanswers=greet)

# @app.route("/askExercise")
# def startTrainerAskExercise():
#     greet = askExercise()
#     if "Great" in greet:
#         demo.start_planks(0)
#     return jsonify(buttonName = "Lets do it!",botanswers=greet)

# @app.route("/trainer")
# def startTrainerForced():
#     demo.start_planks(1)
#     return "nothing"

if __name__ == "__main__":
    # app.run(debug=True) 
    
    socketio.run(app)