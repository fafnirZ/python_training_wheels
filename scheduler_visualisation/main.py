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
    

    def assign_task(self, curr_time: int, task: int):
        _task = (curr_time, curr_time + task)
        self.curr_task = _task
        self.task_log.append(_task)


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
    

    
    #
    for w in workers:
        print(w.task_log)

    



if __name__ == "__main__":
    main()