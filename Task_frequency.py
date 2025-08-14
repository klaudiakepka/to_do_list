from datetime import datetime, timedelta
from Task import Task

class Task_frequency(Task):
    def __init__(self, name, state, date, streak, frequency):
        super().__init__(name, state, streak)
        self.date = date
        self.frequency = frequency

    def show(self):
        today = datetime.today().date()
        return self.date + timedelta(days=int(self.frequency)) <= today or self.date == today

    def get_frequency(self):
        return self.frequency

    def get_date(self):
        return self.date