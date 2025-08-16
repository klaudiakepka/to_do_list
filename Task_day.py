from datetime import datetime
from Task import Task

class Task_day(Task):
    def __init__(self,type, name, state, streak, day):
        super().__init__(type, name, state, streak)
        self.day = day

    def show(self):
        today = datetime.today().day
        return self.day == today

    def write(self):
        return f"{self.type},{self.name},{self.state.get()},{self.streak},{self.day}"
