from Task import Task

class Task_list(Task):
    def __init__(self,type, name, state, streak, main_task, tasks=None):
        super().__init__(type, name, state, streak)
        self.main_task = main_task
        self.tasks = tasks if tasks is not None else []

    def mark_main_task(self):
        mark = True
        for task in self.tasks:
            if not task.get_state_get():
                mark = False
        if mark:
            self.state.set(True)

    def get_tasks(self):
        return self.tasks

    def get_main_task(self):
        return self.main_task