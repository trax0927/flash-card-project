from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

#-----------------------retriving-information--------------------#
try:
    left_words = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("./data/french_words.csv")
    data_dict = df.to_dict(orient="records")
else:
    data_dict = left_words.to_dict(orient="records")

random_words = {}


def get_items():
    global random_words, timer
    window.after_cancel(timer)
    random_words = random.choice(data_dict)
    french_word = random_words["French"]
    canva.itemconfig(card_word, fill="black", text=french_word)
    canva.itemconfig(card_language, fill="black", text="French")
    canva.itemconfig(card_image, image=image_front)
    timer = window.after(3000, turn_back)
    print(random_words)


def known_words():
    global random_words
    data_dict.remove(random_words)
    remaining_words = [words_left for words_left in data_dict]
    new_df = pd.DataFrame(remaining_words)
    new_df.to_csv("./data/words_to_learn.csv", index=False)


def right_button_combined():
    get_items()
    known_words()


def turn_back():
    global random_words
    canva.itemconfig(card_image, image=image_back)
    english_word = random_words["English"]
    canva.itemconfig(card_word, fill="white", text=english_word)
    canva.itemconfig(card_language, fill="white", text="English")

#-----------------------UI SETUP---------------------------------#


window = Tk()
window.title("flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, turn_back)

canva = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
image_back = PhotoImage(file="./images/card_back.png")
image_front = PhotoImage(file="./images/card_front.png")
card_image = canva.create_image(410, 273, image=image_front)
card_word = canva.create_text(400, 263, text="", fill="black", font=("Ariel", 69, "bold"))
card_language = canva.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
canva.grid(row=1, column=1, columnspan=2)

right_image = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=right_button_combined)
right_btn.grid(row=2, column=2)
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=get_items)
wrong_btn.grid(row=2, column=1)

get_items()

window.mainloop()
