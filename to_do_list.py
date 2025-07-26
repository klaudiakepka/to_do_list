from datetime import datetime
from tkinter import *
from tkinter import simpledialog
from Task import Task

def load(_list):
    _list.clear()
    with open('dane/zadania.txt', encoding='utf-8') as file:
        for text_line in file.readlines():
            parts = text_line.split(',')
            _list.append(Task(parts[0], parts[1], parts[2], parts[3]))
    checkboxes = []
    for widget in container.winfo_children():
        widget.destroy()
    for task in _list:
        checkboxes.append(Checkbutton(container, text=task.get_name(), variable=task.get_state()))
    for i in range(len(checkboxes)):
        checkboxes[i].pack(anchor='w')

def add():
    save_state(tasks)
    user_input = get_input()
    today = datetime.today()
    write = True
    if user_input is None:
        write = False
    elif len(user_input) <= 0:
        write = False
    elif "\\n" in user_input:
        write = False
    else:
        for item in tasks:
            if item.get_name() == user_input:
                write = False
                print(f"already exists")

    with open('dane/zadania.txt', 'a', encoding='utf-8') as file:
        if write:
            file.write(f"{user_input},0,{today.day},0,\n")
        else:
            print(f"failed")
    load(tasks)

def delete():
    name = get_input()
    change = False
    for item in tasks:
        if name == item.get_name():
            tasks.remove(item)
            change = True
            print("removed")
    if change:
        save_state(tasks)
    load(tasks)

def save_state(_list):
    today = datetime.today()
    with open('dane/zadania.txt', 'w', encoding='utf-8') as file:
        for item in _list:
            file.write(f"{item.get_name()}{f",1,{today.day},{item.get_streak()},\n" if item.get_state_get() else f",0,{today.day},{item.get_streak()},\n"}")

def open_new_day(_list):
    today = datetime.today()
    if int(_list[0].get_day()) != today.day:
        for item in _list:
            if item.get_state_get():
                item.add_streak()
            else:
                item.break_streak()
            item.change_state()

def get_input():
    user_input = simpledialog.askstring("Wprowadź dane", "Wpisz tekst:")
    return user_input

root = Tk()
container = Frame(root)
container.grid(row=1, columnspan=3, sticky='w')

tasks = []
load(tasks)
open_new_day(tasks)

add_button = Button(root, text="add", command=add)
add_button.grid(row=0, column=0)
remove_button = Button(root, text="remove", command=delete)
remove_button.grid(row=0, column=1)

root.mainloop()
save_state(tasks)