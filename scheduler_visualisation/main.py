from dataclasses import dataclass, field


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
    

    def assign_task(self, *, curr_time: int, task: int, task_id: int|None):
        _task = (curr_time, curr_time + task, task_id)
        self.curr_task = _task
        self.task_log.append(_task)





def strategy_1_perfect_scheduling(tasks: list, workers:list):
    t = 0
    while tasks:
        for worker in workers:
            if worker.is_free(t):
                try:
                    _tsk = tasks.pop()
                    worker.assign_task(curr_time=t, task=_tsk, task_id=_tsk)
                except IndexError:
                    break
        t+=1


def strategy_2_bottlenecked_by_slowest(tasks: list, workers: list):
    t = 0
    def is_all_workers_in_batch_complete(workers, curr_time):
        for worker in workers:
            if not worker.is_free(curr_time):
                return False
        return True
    while tasks:
        if is_all_workers_in_batch_complete(workers, t):
            for worker in workers:
                if worker.is_free(t):
                    try:
                        _tsk = tasks.pop()
                        worker.assign_task(curr_time=t, task=_tsk, task_id=_tsk)
                    except IndexError:
                        break
        else:
            for worker in workers:
                if not worker.is_free(t):
                    worker.assign_task(curr_time=t, task=1, task_id=None)
                
        t+=1

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

        elif colour == "clear":
            C_ = CLEAR

        print(f"{C_}{ColouredBlock.content}{CLEAR}", end="")




def main():

    tasks = []
    for _ in range(100):
        tasks.append(1)
        tasks.append(2)
        tasks.append(3)
        tasks.append(4)

    n_workers = 32
    # main loop

    workers = [
        Worker(id=i)
        for i in range(n_workers)
    ]

    #
    # strategy_1_perfect_scheduling(tasks, workers)
    strategy_2_bottlenecked_by_slowest(tasks, workers)


    task_colours = {
        1: "blue",
        2: "green",
        3: "red",
        4: "yellow",
        None: "clear",
    }
    for worker in workers:
        print(f"Worker: {worker.id}  ",end="")
        for record in worker.task_log:
            task_id = record[2]
            task_colour = task_colours[task_id]
            task_duration = record[1]-record[0]
            for _ in range(task_duration):
                ColouredBlock.display(task_colour)
        print("")

if __name__ == "__main__":
    main()