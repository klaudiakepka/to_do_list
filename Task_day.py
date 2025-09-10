from datetime import datetime
from Task import Task

class Task_day(Task):
    def __init__(self, type, name, state, streak, date, week_days):
        super().__init__(type, name, state, streak, date)
        self.week_days = week_days

    def show(self):
        today = datetime.today().date()
        if str(today.weekday()) in self.week_days and self.date <= today:
            return True
        return False

    def write(self,date=None):
        if date is None:
            date = self.date
        return f"{self.type},{self.name},{self.state.get()},{self.streak},{date},{self.week_days},\n"
