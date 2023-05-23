from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0  # 2 consecutive reps includes 25min work + 5min shortbreak, after 7 reps there'll be a rep of longbreak
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def handle_reset():
    global timer
    global reps
    title.config(text="Pomodoro Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    window.after_cancel(timer)
    reps = 0  # reset reps


# ---------------------------- TIMER MECHANISM ------------------------------- #
def handle_start():
    global reps
    reps += 1

    # render check_marks
    if reps % 2 == 0:  # if completed a work section, add a check mark
        work_sections = reps // 2
        marks = ""
        for _ in range(work_sections):
            marks += "✓"
        check_marks.config(text=marks)

    # render clock
    if reps == 1:
        count_down(WORK_MIN * 60)
        title.config(text="Work", fg=GREEN)

    elif reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title.config(text="Long Break", fg=RED)

    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title.config(text="Short Break", fg=PINK)

    else:
        count_down(WORK_MIN * 60)
        title.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    min = count // 60  # floor division
    sec = count % 60
    if min < 10:
        min = f"0{min}"
    if sec < 10:
        sec = f"0{sec}"

    canvas.itemconfig(timer_text, text=f"{min}:{sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)  # call countdown(count-1) after 1000 miliseconds, this is like recursive function with timer
    else:
        handle_start()  # automatically start new rep when a rep is done


# ---------------------------- UI SETUP ------------------------------- #
# set up screen
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# Canvas: allows to layer objects on top of each other (here we place the timer text on top of tomato image)
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")  # this image is 200x223px
timer_img = canvas.create_image(100, 112, image=tomato_img)  # place image in middle of canvas at coor (103,112)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=2, row=2)


# title Label
title = Label(text="Pomodoro Timer", bg=YELLOW, fg=GREEN, font=("Ariel", 50, "bold"))  # fg (foreground) is font color
title.grid(column=2, row=1)


# button
start_button = Button(text="Start", highlightthickness=0, font=(FONT_NAME, 20, "bold"), command=handle_start)
start_button.grid(column=1, row=3)

reset_button = Button(text="Reset", highlightthickness=0, font=(FONT_NAME, 20, "bold"), command=handle_reset)
reset_button.grid(column=3, row=3)

# check mark label
check_marks = Label(text="", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 24, "bold"))
check_marks.grid(column=2, row=4)

window.mainloop()
