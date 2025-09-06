import os.path
from datetime import datetime, timedelta
from tkinter import *
from Task import Task
from Task_frequency import Task_frequency

def load(_list):
    _list.clear()
    if not os.path.exists('dane/tasks.txt'):
        open('dane/tasks.txt', 'a').close()
    with open('dane/tasks.txt', encoding='utf-8') as file:
        for text_line in file.readlines():
            parts = text_line.split(',')
            if parts[0] == '0':
                _list.append(Task(parts[0], parts[1], parts[2], parts[3], datetime.strptime(parts[4], "%Y-%m-%d").date()))
            elif parts[0] == '1':
                _list.append(Task_frequency(parts[0], parts[1], parts[2], parts[3], datetime.strptime(parts[4], "%Y-%m-%d").date(), parts[5]))

    checkboxes = {}
    for widget in container.winfo_children():
        widget.destroy()
    for task in _list:
        if task.show():
            checkboxes[task.get_name()] = (Checkbutton(container, text=task.get_name(), variable=task.get_state()))
            checkboxes[task.get_name()].pack(anchor='w')

def add():
    expanded_frequency = False
    expanded_date = False

    def toggle_frequency():
        nonlocal expanded_frequency
        if not expanded_frequency:
            arrow_frequency.config(text="▼ frequency")
            frequency_label.grid(row=2, column=0, sticky=W)
            frequency_entry.grid(row=2, column=1)
            arrow_date.grid(row=frequency_entry.grid_info()["row"]+1)
            expanded_frequency = True
        else:
            arrow_frequency.config(text="▶ frequency")
            frequency_label.grid_remove()
            frequency_entry.grid_remove()
            expanded_frequency = False

    def toggle_date():
        nonlocal expanded_date
        if not expanded_date:
            arrow_date.config(text="▼ date")
            row = arrow_date.grid_info()['row']
            date_label.grid(row=row+1, column=0, sticky=W)
            date_entry.grid(row=row+1, column=1)
            error_message.grid(row=row+2)
            expanded_date = True
        else:
            arrow_date.config(text="▶ date")
            date_label.grid_remove()
            date_entry.grid_remove()
            expanded_date = False

    def submit():
        date = ""
        frequency = 0
        name = name_entry.get()
        save_state(tasks)
        write = True

        if name is None:
            write = False
            error_message.config(text = "name cannot be empty")
        elif len(name) <= 0:
            write = False
            error_message.config(text = "name cannot be empty")
        elif "\\n" in name:
            write = False
            error_message.config(text = "name cannot contain escape character")
        else:
            for item in tasks:
                if item.get_name() == name:
                    write = False
                    error_message.config(text = "task already exist")

        if expanded_date:
            try:
                date = datetime.strptime(date_entry.get(), "%Y.%m.%d").date()
            except ValueError:
                error_message.config(text = "wrong date. Use format Y.M.D")
                write = False

        if expanded_frequency:
            try:
                frequency = int(frequency_entry.get())
                if frequency <= 0:
                    write = False
                    error_message.config(text = "frequency must be more than 0")
            except (TypeError, ValueError):
                write = False
                error_message.config(text = "frequency must be a number")

        if not os.path.exists('dane/tasks.txt'):
            open('dane/tasks.txt', 'a').close()
        with open('dane/tasks.txt', 'a', encoding='utf-8') as file:
            if write:
                if expanded_frequency:
                    task = Task_frequency(1,name,False,0,date,frequency)
                else:
                    task = Task(0,name,False,0,date)
                file.write(task.write())
                error_message.config(text="")
        load(tasks)

    add_window = Toplevel(root)
    name_label = Label(add_window, text="name:")
    arrow_frequency = Label(add_window, text='▶ frequency')
    frequency_label = Label(add_window, text="frequency:")
    arrow_date = Label(add_window, text="▶ date")
    date_label = Label(add_window, text='starting date:')
    name_entry = Entry(add_window)
    frequency_entry = Entry(add_window)
    date_entry = Entry(add_window)
    submit_button = Button(add_window, text="Submit", command=submit)
    error_message = Label(add_window, text="")


    name_label.grid(row=0, column=0, sticky=W)
    arrow_frequency.grid(row=1, column=0, sticky=W)
    frequency_label.grid(row=2, column=0, sticky=W)
    arrow_date.grid(row=3, column=0, sticky=W)
    date_label.grid(row=5, column=0, sticky=W)
    name_entry.grid(row=0, column=1)
    frequency_entry.grid(row=2, column=1)
    date_entry.grid(row=3, column=1)
    submit_button.grid(row=0, column=2, rowspan=arrow_date.grid_info()["row"]+2)
    error_message.grid(row=4, column=0, columnspan=3)

    arrow_frequency.bind("<Button-1>", lambda e: toggle_frequency())
    arrow_date.bind("<Button-1>", lambda e: toggle_date())
    frequency_label.grid_remove()
    date_label.grid_remove()
    frequency_entry.grid_remove()
    date_entry.grid_remove()

def delete():
    def create():
        name_list.delete(0, END)
        for i in range(len(tasks)):
            name_list.insert(i, tasks[i].get_name())

    def submit():
        name = name_list.get(name_list.curselection())
        for item in tasks:
            if name == item.get_name():
                tasks.remove(item)
                message.config(text=f"{name} removed")
                save_state(tasks)
                create()
        load(tasks)

    delete_window = Toplevel(root)
    name_list = Listbox(delete_window)
    delete_button = Button(delete_window, text="delete", command=submit)
    message = Label(delete_window, text="")
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
            file.write(item.write(date))

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