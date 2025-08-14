import os.path
from datetime import datetime, timedelta
from tkinter import *
from Task_frequency import Task_frequency


def load(_list):
    _list.clear()
    if not os.path.exists('dane/tasks.txt'):
        open('dane/tasks.txt', 'a').close()
    with open('dane/tasks.txt', encoding='utf-8') as file:
        for text_line in file.readlines():
            parts = text_line.split(',')
            _list.append(Task_frequency(parts[0], parts[1], datetime.strptime(parts[2], "%Y-%m-%d").date(), parts[3], parts[4]))

    checkboxes = []
    for widget in container.winfo_children():
        widget.destroy()
    for task in _list:
        if task.show():
            checkboxes.append(Checkbutton(container, text=task.get_name(), variable=task.get_state()))
    for i in range(len(checkboxes)):
        checkboxes[i].pack(anchor='w')

def add():
    error = StringVar()

    def submit():
        date = ""
        frequency = 0
        name = name_entry.get()
        save_state(tasks)
        write = True
        try:
            date = datetime.strptime(date_entry.get(), "%Y.%m.%d").date()
        except ValueError:
            error.set("wrong date. Use format Y.M.D")
            write = False

        try:
            frequency = int(frequency_entry.get())
            if frequency <= 0:
                write = False
                error.set("frequency must be more than 0")
        except (TypeError, ValueError):
            write = False
            error.set("frequency must be a number")
        if name is None:
            write = False
            error.set("name cannot be empty")
        elif len(name) <= 0:
            write = False
            error.set("name cannot be empty")
        elif "\\n" in name:
            write = False
            error.set("name cannot contain escape character")
        else:
            for item in tasks:
                if item.get_name() == name:
                    write = False
                    error.set("task already exist")

        if not os.path.exists('dane/tasks.txt'):
            open('dane/tasks.txt', 'a').close()
        with open('dane/tasks.txt', 'a', encoding='utf-8') as file:
            if write:
                file.write(f"{name},0,{date.isoformat()},0,{frequency},\n")
        load(tasks)

    add_window = Toplevel(root)
    name_label = Label(add_window, text="name:")
    frequency_label = Label(add_window, text="frequency:")
    date_label = Label(add_window, text='starting date:')
    name_entry = Entry(add_window)
    frequency_entry = Entry(add_window)
    date_entry = Entry(add_window)
    submit_button = Button(add_window, text="Submit", command=submit)
    error_message = Label(add_window, textvariable=error)

    name_label.grid(row=0, column=0, sticky=W)
    frequency_label.grid(row=1, column=0, sticky=W)
    date_label.grid(row=2, column=0, sticky=W)
    name_entry.grid(row=0, column=1)
    frequency_entry.grid(row=1, column=1)
    date_entry.grid(row=2, column=1)
    submit_button.grid(row=0, column=2, rowspan=3)
    error_message.grid(row=3, column=0, columnspan=3)

def delete():
    text = StringVar()

    def create():
        name_list.delete(0, END)
        for i in range(len(tasks)):
            name_list.insert(i, tasks[i].get_name())

    def submit():
        name = name_list.get(name_list.curselection())
        change = False
        for item in tasks:
            if name == item.get_name():
                tasks.remove(item)
                change = True
                text.set("Task removed")
        if change:
            save_state(tasks)
            create()
        load(tasks)

    delete_window = Toplevel(root)
    name_list = Listbox(delete_window)
    delete_button = Button(delete_window, text="delete", command=submit)
    message = Label(delete_window, textvariable=text)
    create()
    name_list.grid(column=0, row=0)
    delete_button.grid(column=1, row=0)
    message.grid(columnspan=2, row=2)

def save_state(_list):
    today = datetime.today().date()
    if not os.path.exists('dane/tasks.txt'):
        open('dane/tasks.txt', 'a').close()
    with open('dane/tasks.txt', 'w', encoding='utf-8') as file:
        for item in _list:
            if item.show() and not item.get_state_get() :
                date = item.get_date()
            elif item.show():
                date = today
            else:
                date = item.get_date()
            file.write(f"{item.get_name()},{f"1" if item.get_state_get() else f"0"},{date.isoformat()},{item.get_streak()},{item.get_frequency()},\n")

def open_new_day(_list):
    today = datetime.today().date()
    if not os.path.exists('dane/current_date.txt'):
        with open('dane/current_date.txt', 'a+') as file:
            file.write(today.isoformat())
    with open('dane/current_date.txt', 'r+') as file:
        date = datetime.strptime(file.read(), "%Y-%m-%d").date()
        while date != today:
            date += timedelta(days=1)
            for item in _list:
                if item.show():
                    if item.get_state_get():
                        item.add_streak()
                        item.change_state()
                    else:
                        item.break_streak()
        file.seek(0)
        file.write(date.isoformat())
        file.truncate()


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