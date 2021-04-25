import tkinter as tk
from tkinter import *
import time
import random
import threading

root = tk.Tk()
root.title("MentalMathApp")
canvas = tk.Canvas(root, height=400, width=400, bg="#ffffff")
root.resizable(False, False)
canvas.grid(columnspan=2, rowspan=5)

user_input = StringVar()
calculation = StringVar(value="Click on Start to begin")
countdown_string = StringVar(value="01:00")
score_counter = StringVar(value="0")

result = 0
playing = False


def manage_game():
    global playing
    if playing == False:
        playing = True
        start_game()
    else:
        playing = False
        end_game()


def start_game():
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
    start_button["text"] = "Start"
    calcul_text["font"] = "SansSerif, 18"
    calcul_text["padx"] = 50
    calcul_text["pady"] = 20
    calculation.set("Game stopped")
    countdown_string.set("01:00")
    solution_input["state"] = tk.DISABLED


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
        calculation.set("Time's up!")
        end_game()


def generate_calculation():
    global result
    rd_nb = round(random.uniform(0, 10), 2)
    if rd_nb <= 2.5:
        operation = " + "
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        result = x + y
    elif rd_nb <= 5:
        operation = " - "
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        result = x - y
    else:
        operation = " x "
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        result = x * y

    print(x, operation, y, "=", result)
    calculation.set(str(x) + operation + str(y) + " =")


def check_input(key):
    try:
        if result == int(solution_input.get()):
            solution_input.delete(0, END)
            generate_calculation()
            current_score = int(score_counter.get())
            current_score = current_score + 5
            score_counter.set(str(current_score))
    except:
        print("input was not a valide integer")
        return


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
operation_params = {
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
calcul_text = tk.Label(root, **operation_params, textvariable=calculation)
solution_input = tk.Entry(
    root,
    **input_params,
    textvariable=user_input,
    state="disabled",
)
score_title = tk.Label(root, **text_params, text="Score")
score = tk.Label(root, **text_params, textvariable=score_counter)
best_title = tk.Label(root, **text_params, text="Best")
best = tk.Label(root, **text_params, text="0")

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
