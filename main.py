from tkinter import *
from random import randint, choice
import pandas

# CONSTANTS
BACKGROUND_COLOR = "#B1DDC6"
WORD_FONT = ("Ariel", 60, "bold")
WORD_POS = (400, 263)
LANG_FONT = ("Ariel", 40, "italic")
LANG_POS = (400, 150)
TIME = 1000
ans = None
german = None
english = None

# MECHANISM
try:
    datafile = pandas.read_csv("data/words_to_learn.csv")

except:
    datafile = pandas.read_csv("data/German500.csv")
choice_dict = {row["German"]: row["English"] for (index, row) in datafile.iterrows()}
choice_list = [key for (key, values) in choice_dict.items()]


def update(cl):
    update_dict = {
        "German": cl,
        "English": [values for (key, values) in choice_dict.items()]
    }
    data = pandas.DataFrame(update_dict)
    data.to_csv("data/words_to_learn.csv")


def showeng(eng):
    canvas.itemconfig(picture, image=back_photo)
    canvas.itemconfig(word, text=eng, fill="white")
    canvas.itemconfig(lang, text="English", fill="white")


def choosenext():
    global ans
    try:
        window.after_cancel(ans)
        canvas.itemconfig(picture, image=front_photo)
    except ValueError:
        pass
    global german, english
    german = choice(choice_list)
    english = choice_dict[german]
    canvas.itemconfig(word, text=german, fill="black")
    canvas.itemconfig(lang, text="German", fill="black")
    ans = window.after(TIME * 5, showeng, english)


def correct():
    global german, english
    try:
        choice_list.remove(german)
        choice_dict.pop(german)
        update(choice_list)
    except ValueError:
        pass
    choosenext()


# UI
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

front_photo = PhotoImage(file="images/card_front.png")
back_photo = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
picture = canvas.create_image(400, 263, image=front_photo)
word = canvas.create_text(WORD_POS[0], WORD_POS[1], text="Word", font=WORD_FONT)
lang = canvas.create_text(LANG_POS[0], LANG_POS[1], text="Title", font=LANG_FONT)
canvas.grid(row=0, column=0, rowspan=2, columnspan=2)

photo_right = PhotoImage(file="images/right.png")
photo_wrong = PhotoImage(file="images/wrong.png")
right = Button(image=photo_right, highlightthickness=0, bg=BACKGROUND_COLOR, command=correct)
wrong = Button(image=photo_wrong, highlightthickness=0, bg=BACKGROUND_COLOR, command=choosenext)
right.grid(row=2, column=0)
wrong.grid(row=2, column=1)

window.mainloop()
