#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
import string

root = Tk()

lbFont = ("Helvetica", 16)
lbHeight = 30
picked = ""

exclusions_set = set()
with open("exclusions.exc", "r") as f:
    exclusions = f.read()
    exclusions_set = set(exclusions.split())


def clear_text(text, chars):
    char_list = list(chars)
    cleaned_text = ""
    for ch in char_list:
        cleaned_text = text.replace(ch, " ")
        text = cleaned_text
    return cleaned_text


def open_subtitles():
    name = filedialog.askopenfilename(
        initialdir="./subtitles",
        filetypes=(("subtitles files", "*.srt"), ("all files", "*.*")),
        title="Open file",
    )
    with open(name, "r") as f:
        text = f.read()
        text = clear_text(
            text, r'.-;:"&,0123456789%<>/\\!?'
        )  # TODO: replase with regex: remove not words etc.
        words = text.split()
        my_set = set(words) - exclusions_set
        lb1.delete(0, END)
        for word in sorted(my_set):
            if len(word) > 2:
                lb1.insert(END, word)


def save_picked_words():
    name = filedialog.asksaveasfilename(
        initialdir=".",
        title="Save file",
        filetypes=(("text files", "*.txt"), ("all files", "*.*")),
    )
    with open(name, "w") as f:
        for item in get_picked_words():
            f.write(f"{item}\n")


def save_exclusions():
    new_exclusions_set = set(get_new_exclusions())
    all_exclusions = exclusions_set | new_exclusions_set
    with open("exclusions.exc", "w") as f:
        for item in all_exclusions:
            f.write(f"{item}\n")


def show_exclusions():
    lb1.delete(0, END)
    for word in sorted(exclusions_set):
        lb1.insert(END, word)


def lb1_click(event):
    widget = event.widget
    selection = widget.curselection()
    picked = widget.get(selection)
    lb1.delete(selection[0])
    lb2.insert(END, picked)


def lb2_click(event):
    widget = event.widget
    selection = widget.curselection()
    picked = widget.get(selection)
    lb2.delete(selection[0])
    lb1.insert(END, picked)


def get_picked_words():
    return lb2.get(0, END)


def get_new_exclusions():
    return lb1.get(0, END)


Title = root.title("Subtitles word picker")

# Menu Bar
menu = Menu(root)
root.config(menu=menu)
file = Menu(menu)
file.add_command(label="Open subtitles", command=open_subtitles)
file.add_command(label="Save picked words", command=save_picked_words)
file.add_command(label="Show exclusions", command=show_exclusions)
file.add_command(label="Save exclusions", command=save_exclusions)
file.add_command(label="Exit", command=lambda: exit())
menu.add_cascade(label="File", menu=file)


lb1 = Listbox(root, font=lbFont, height=lbHeight)
lb1.bind("<Double-1>", lb1_click)
lb1.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

sb1 = Scrollbar(root)
sb1.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
lb1.config(yscrollcommand=sb1.set)
sb1.config(command=lb1.yview)

lb2 = Listbox(root, font=lbFont, height=lbHeight)
lb2.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
lb2.bind("<Double-1>", lb2_click)

sb2 = Scrollbar(root)
sb2.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
lb2.config(yscrollcommand=sb2.set)
sb2.config(command=lb2.yview)

root.mainloop()
