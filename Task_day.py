from datetime import datetime
from Task import Task


class Task_day(Task):
    def __init__(self, name, state, streak, day):
        super().__init__(name, state, streak)
        self.day = day

    def show(self):
        today = datetime.today().day
        return self.day == today

    def get_day(self):
        return self.day
