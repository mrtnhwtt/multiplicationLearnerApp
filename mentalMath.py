import tkinter as tk
from tkinter import *
import time
import random
import threading
import os

root = tk.Tk()
root.title("MentalMathApp")
canvas = tk.Canvas(root, height=400, width=400, bg="#ffffff")
root.resizable(False, False)
canvas.grid(columnspan=2, rowspan=5)

user_input = StringVar()
calculation = StringVar(value="Click on Start to begin")
countdown_string = StringVar(value="01:00")
score_counter = StringVar(value="0")

if os.path.isfile("score.txt"):
    with open("score.txt", "r") as f:
        hightscore = f.read()
    score_best = StringVar(value=str(hightscore))
else:
    score_best = StringVar(value="0")

result = 0
playing = False
start_time = 0
operator = ""


def manage_game():
    if playing == False:
        start_game()
    else:
        end_game()


def start_game():
    global playing
    playing = True
    score_counter.set("0")
    solution_input["state"] = tk.NORMAL
    start_button["text"] = "Stop"
    calcul_text["font"] = "SansSerif, 25"
    calcul_text["padx"] = 26
    calcul_text["pady"] = 10
    solution_input.focus()
    countdown_thread = threading.Thread(target=countdown, args=[60], daemon=True)
    countdown_thread.start()
    generate_calculation()


def end_game():
    global playing
    playing = False
    start_button["text"] = "Start"
    calcul_text["font"] = "SansSerif, 18"
    calcul_text["padx"] = 50
    calcul_text["pady"] = 20
    countdown_string.set("01:00")
    solution_input["state"] = tk.DISABLED
    manage_score()


def manage_score():
    current_score = int(score_counter.get())
    best_score = int(score_best.get())
    if current_score > best_score:
        score_best.set(current_score)
        calculation.set("New Hight Score : %s" % (str(current_score)))
        with open("score.txt", "w") as f:
            f.write(str(current_score))
    else:
        calculation.set("Game ended. Score : %s" % (str(current_score)))


def countdown(t):
    finished = False
    while t >= 0 and playing == True:
        mins = t // 60
        secs = t % 60
        timer = "{:02d}:{:02d}".format(mins, secs)
        countdown_string.set(timer)
        time.sleep(1)
        t -= 1
        if t == 0:
            finished = True
    if finished:
        end_game()


def generate_calculation():
    global result, start_time, operator
    rd_nb = round(random.uniform(0, 10), 2)
    if rd_nb <= 2.5:
        operator = "+"
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        result = x + y
    elif rd_nb <= 5:
        operator = "-"
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        result = x - y
    else:
        operator = "x"
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        result = x * y

    print(x, operator, y, "=", result)
    calculation.set(str(x) + " " + operator + " " + str(y) + " =")
    start_time = time.time()


def check_input(key):
    inputed_answer = solution_input.get()
    try:
        inputed_answer = int(inputed_answer)
    except:
        print("input was not a valide integer")
        return
    if result == int(solution_input.get()):
        solution_input.delete(0, END)
        current_score = int(score_counter.get())
        points = calculate_point()
        new_score = current_score + points
        score_counter.set(str(new_score))
        generate_calculation()


def calculate_point():
    max_point = 10
    multiplier = 1
    time_elapsed = round(time.time() - start_time, 2)
    if operator == "x":
        multiplier = 1.5
    points = round(max_point * multiplier - time_elapsed)
    if points < 1:
        points = 1
    return points


btn_params = {
    "padx": 25,
    "pady": 0,
    "bd": 2,
    "fg": "black",
    "bg": "#C7DBB1",
    "font": ("Sans-serif", 13),
    "width": 2,
    "height": 2,
    "relief": "flat",
    "activebackground": "#5CB85C",
}
text_params = {
    "padx": 50,
    "pady": 0,
    "bd": 4,
    "fg": "grey",
    "bg": "#fff",
    "font": ("Sans-serif", 18),
    "width": 4,
    "height": 2,
}
operator_params = {
    "padx": 50,
    "pady": 20,
    "bd": 4,
    "fg": "grey",
    "bg": "#fff",
    "font": ("Sans-serif", 18),
    "width": 8,
    "height": 2,
    "wraplength": 200,
}
input_params = {
    "width": 5,
    "justify": "left",
    "borderwidth": 15,
    "relief": tk.FLAT,
    "highlightthickness": 0,
    "font": ("Sans-serif", 18),
    "disabledbackground": "#fff",
}


timer_label = tk.Label(root, **text_params, textvariable=countdown_string)
start_button = tk.Button(
    root, **btn_params, text="Start", command=lambda: manage_game()
)
calcul_text = tk.Label(root, **operator_params, textvariable=calculation)
solution_input = tk.Entry(
    root,
    **input_params,
    textvariable=user_input,
    state="disabled",
)
score_title = tk.Label(root, **text_params, text="Score")
score = tk.Label(root, **text_params, textvariable=score_counter)
best_title = tk.Label(root, **text_params, text="Best")
best = tk.Label(root, **text_params, textvariable=score_best)

solution_input.bind("<KeyRelease>", check_input)

timer_label.grid(column=0, row=0)
start_button.grid(column=1, row=0)
calcul_text.grid(column=0, row=2)
solution_input.grid(column=1, row=2)
score_title.grid(column=0, row=3, sticky="s")
score.grid(column=0, row=4, sticky="n")
best_title.grid(column=1, row=3, sticky="s")
best.grid(column=1, row=4, sticky="n")


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)


root.mainloop()
