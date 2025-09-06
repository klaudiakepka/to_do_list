from datetime import datetime
from Task import Task

class Task_day(Task):
    def __init__(self, type, name, state, streak, date, week_days):
        super().__init__(type, name, state, streak, date)
        self.week_days = week_days

    def show(self):
        today = datetime.today().date()
        if today.weekday() in self.week_days and self.date <= today:
            return True
        return False
