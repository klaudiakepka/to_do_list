from Task import Task

class Task_list(Task):
    def __init__(self,type, name, state, streak, date, sub_task_num):
        super().__init__(type, name, state, streak, date)
        self.tasks = []
        self.sub_task_num = sub_task_num

    def mark_main_task(self):
        mark = True
        for task in self.tasks:
            if not task.get_state_get():
                mark = False
        if mark:
            self.state.set(True)

    def get_subtasks(self):
        return self.tasks

    def add_subtask(self, subtask):
        self.tasks.append(subtask)