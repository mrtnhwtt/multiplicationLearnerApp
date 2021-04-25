import tkinter as tk
from tkinter import *
import time
import random
import threading

root = tk.Tk()
root.title("MentalMathApp")
canvas = tk.Canvas(root, height=700, width=600, bg='#ffffff')
root.resizable(False, False)
canvas.grid(columnspan=4, rowspan=5)

user_input = StringVar()
calculation = StringVar(value='Click on Start to begin')
countdown_string = StringVar(value="01:00")
score_counter = StringVar()

result = 0
playing = False


def manage_game():
    global playing
    if(playing == False):
        playing = True
        start_game()
    else:
        playing = False
        end_game()


def start_game():
    score_counter.set("0")
    solution_input['state'] = tk.NORMAL
    start_button['text'] = 'Stop'
    solution_input.focus()
    countdown_thread = threading.Thread(target=countdown, args=[60])
    countdown_thread.start()
    generate_calculation()


def end_game():
    start_button['text'] = 'Start'
    calculation.set("Game stopped")
    countdown_string.set("01:00")
    solution_input['state'] = tk.DISABLED


def countdown(t):
    finished = False
    try:
        while t >= 0 and playing == True:
            mins = t // 60
            secs = t % 60
            timer = '{:02d}:{:02d}'.format(mins, secs)
            countdown_string.set(timer)
            time.sleep(1)
            t -= 1
            if(t == 0):
                finished = True
        if finished:
            calculation.set("Time's up!")
            end_game()
    except:
        print('Program was closed while the timer was running')


def generate_calculation():
    global result
    rd_nb = round(random.uniform(0, 10), 2)
    if(rd_nb <= 2.5):
        operation = '+'
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        result = x + y
    elif(rd_nb <= 5):
        operation = '-'
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        result = x - y
    else:
        operation = 'x'
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        result = x * y

    print(x, operation, y, '=', result)
    calculation.set(str(x) + operation + str(y))


def check_input(key):
    try:
        if(result == int(solution_input.get())):
            solution_input.delete(0, END)
            generate_calculation()
            current_score = int(score_counter.get())
            current_score = current_score + 5
            score_counter.set(str(current_score))
    except:
        print("input was not a valide integer")
        return


timer_label = tk.Label(root, textvariable=countdown_string, bg="#ffffff")
start_button = tk.Button(
    root, text="Start", command=lambda: manage_game())
calcul_text = tk.Label(root, textvariable=calculation, bg="#ffffff")
solution_input = tk.Entry(root, textvariable=user_input,
                          justify="center", width=10, borderwidth=0, state='disabled')
score = tk.Label(root, textvariable=score_counter, bg="#ffffff")
best = tk.Label(root, text="best", bg="#ffffff")

solution_input.bind("<KeyRelease>", check_input)

timer_label.grid(column=1, row=0)
start_button.grid(column=2, row=0)
calcul_text.grid(column=1, row=2)
solution_input.grid(column=2, row=2)
score.grid(column=1, row=4)
best.grid(column=2, row=4)


root.mainloop()
