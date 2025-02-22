from dataclasses import dataclass, field
import plotly.figure_factory as ff


@dataclass
class Worker:
    id: int
    task_log: list = field(default_factory=lambda: [])
    curr_task: int = field(default=None)


    def is_free(self, curr_time: int) -> bool:
        if self.curr_task is None:
            return True
        
        if self.curr_task[0] <= curr_time < self.curr_task[1]:
            return False
        return True
    

    def assign_task(self, curr_time: int, task: int):
        _task = (curr_time, curr_time + task)
        self.curr_task = _task
        self.task_log.append(_task)



class ColouredBlock:
    content = '█'

    @staticmethod
    def display(colour):
        CLEAR = "\033[0m"  # Corrected CLEAR code
        C_ = ""  # Initialize C_
        if colour == "blue":
            C_ = "\033[34m"  # Corrected blue code
        elif colour == "red": #added red example
            C_ = "\033[31m"
        elif colour == "green": #added green example
            C_ = "\033[32m"
        elif colour == "bright_blue":
            C_ = "\033[94m" #bright blue example
        elif colour == "yellow":
            C_ = "\033[33m"

        print(f"{C_}{ColouredBlock.content}{CLEAR}", end="")




def main():

    tasks = []
    for _ in range(100):
        tasks.append(1)
        tasks.append(2)
        tasks.append(3)

    n_workers = 3
    # main loop

    workers = [
        Worker(id=i)
        for i in range(n_workers)
    ]

    t = 0
    while tasks:
        for worker in workers:
            if worker.is_free(t):
                try:
                    _tsk = tasks.pop()
                    worker.assign_task(t, _tsk)
                except IndexError:
                    break
        t+=1
    
    task_colours = {
        1: "blue",
        2: "green",
        3: "red"
    }
    for worker in workers:
        print(f"Worker: {worker.id}  ",end="")
        for record in worker.task_log:
            task_id = record[1]-record[0]
            task_colour = task_colours[task_id]
            for _ in range(task_id):
                ColouredBlock.display(task_colour)
        print("")

if __name__ == "__main__":
    main()