#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
import string

root = Tk()

lbFont = ("Helvetica", 16)
lbHeight = 30
picked = ""


def clear_text(text, chars):
    char_list = list(chars)
    cleaned_text = ""
    for ch in char_list:
        cleaned_text = text.replace(ch, " ")
        text = cleaned_text
    return cleaned_text


# This is where we lauch the file manager bar.
def open_file():
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
        my_set = set(words)
        for word in sorted(my_set):
            if len(word) > 2:
                lb1.insert(END, word)


def save_file():
    name = filedialog.asksaveasfilename(
        initialdir=".",
        title="Save file",
        filetypes=(("text files", "*.txt"), ("all files", "*.*")),
    )
    with open(name, "w") as f:
        for item in get_words():
            f.write(f"{item}\n")


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


def get_words():
    return lb2.get(0, END)


Title = root.title("Subtitles word picker")

# Menu Bar
menu = Menu(root)
root.config(menu=menu)
file = Menu(menu)
file.add_command(label="Open subtitles", command=open_file)
file.add_command(label="Save picked words", command=save_file)
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
