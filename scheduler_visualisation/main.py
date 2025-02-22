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
            C_ = "\033[97m" # Bright white

        print(f"{C_}{ColouredBlock.content}{CLEAR}", end="")




def main():

    tasks = []
    for _ in range(100):
        tasks.append(1)
        tasks.append(2)
        tasks.append(3)

    n_workers = 32
    # main loop

    workers = [
        Worker(id=i)
        for i in range(n_workers)
    ]

    #
    # strategy_1_perfect_scheduling(tasks, workers)
    strategy_2_bottlenecked_by_slowest(tasks, workers)

    ######################
    # printing mechanism #
    ######################
    task_colours = {
        1: "blue",
        2: "green",
        3: "red",
        4: "yellow",
        None: "clear",
    }

    LONGEST_TASK_TIME = -999
    for worker in workers:
        for record in worker.task_log:
            end_time = record[1]
            if end_time > LONGEST_TASK_TIME:
                LONGEST_TASK_TIME = end_time

    
    for worker in workers:
        print(f"Worker: {worker.id:03}  ",end="")
        task_log = worker.task_log.copy()
        t = 0
        curr_task = None
        while t <= LONGEST_TASK_TIME:
            if curr_task is None:
                curr_task = task_log.pop(0)
            if t >= curr_task[1] and len(task_log) > 0:
                curr_task = task_log.pop(0)
            task_id = curr_task[2]
            task_colour = task_colours[task_id]
            if curr_task[0] <= t <= curr_task[1]:
                ColouredBlock.display(task_colour)
            else:
                ColouredBlock.display("clear") # show inefficiency

            t+=1
        print("")

    
    print(f"TOTAL TIME TAKEN: {LONGEST_TASK_TIME}s")

if __name__ == "__main__":
    main()