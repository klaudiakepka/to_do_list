from datetime import datetime, timedelta
from Task import Task

class Task_frequency(Task):
    def __init__(self,type, name, state, streak, date, frequency):
        super().__init__(type, name, state, streak)
        self.frequency = frequency
        if date == "":
            date = datetime.today().date()
        self.date = date

    def show(self):
        today = datetime.today().date()
        return self.date + timedelta(days=int(self.frequency)) <= today or self.date == today

    def write(self,date=None):
        if date is None:
            date = self.date
        return f"{self.type},{self.name},{self.state.get()},{self.streak},{date},{self.frequency}"

    def get_date(self):
        return self.date