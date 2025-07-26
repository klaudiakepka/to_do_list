from tkinter import *

class Task:
    def __init__(self, name, state, date, streak):
        self.name = name
        self.state = BooleanVar()
        self.state.set(state)
        self.date = date
        self.streak = int(streak)

    def show(self):
        print(self.name + ' ' + str(self.state.get()))

    def change_state(self):
        self.state.set(not self.state)

    def add_streak(self):
        self.streak+=1

    def break_streak(self):
        self.streak = 0

    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

    def get_state_get(self):
        return self.state.get()

    def get_day(self):
        return self.date

    def get_streak(self):
        return self.streak