from datetime import datetime
from tkinter import *

class Task:
    def __init__(self, type, name, state, streak, date):
        self.type = type
        self.name = name
        self.state = BooleanVar()
        self.state.set(state)
        self.streak = int(streak)
        if date == "":
            date = datetime.today().date()
        self.date = date

    def show(self):
        return True

    def write(self,date=None):
        if date is None:
            date = self.date
        return f"{self.type},{self.name},{self.state.get()},{self.streak},{date},\n"

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

    def get_type(self):
        return self.type

    def get_date(self):
        return self.date