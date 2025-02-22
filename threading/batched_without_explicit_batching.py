"""
The hypothesis of this implementation is that
it takes less time than the explicit batched process

each of the threads in the threadpool will 
continuously look for the next job to perform its operation on
this is automatically handled by the threadpool

the only downside to this is that if you try to
create N requests at once its a huge overhead.
so you should still batch it but you should probably make the batch
fairly big i.e. DEFINITELY than the number of workers. 


this is the same as scheduler_visualisation.strategy_1_perfect_scheduling
whereas the other batched.py implementation is more inline with scheduler_visualisation.strategy_2_bottlenecked_by_slowest


implementation3 ---- TODO
workers pull from queue follows a different pattern.
here we manage jobs and submitting jobs to pre-managed threads where scheduling is automatically
handled by the concurrent.futures library.

in workers_pull_from_queue we will be creating the threads and managing the scheduling ourselves
by making the threads run on separate event loops and have them interact with a queue (queue should also be in another thread)
we need to ensure nothing is bottlenecked... not sure yet
"""

import concurrent.futures
import time
from tqdm import tqdm


def worker(results, sleep_time):
    time.sleep(sleep_time)
    results.append(1)


def main():
    n_threads = 3
    job_queue = []
    results = []
    for i in range(10):
        job_queue.append({"sleep_time": 1})
        job_queue.append({"sleep_time": 2})
        job_queue.append({"sleep_time": 3})


    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        
        pbar = tqdm(
            total=len(job_queue)
        )

        futures = []
        for job in job_queue:
            futures.append(
                executor.submit(
                    worker,
                    results,
                    **job,
                )
            )
            
        for future in concurrent.futures.as_completed(futures):
            future.result()
            pbar.update(1)
    
        pbar.close()


if __name__ == "__main__":
    t_0 = time.time()
    main()
    t_1 = time.time()
    print(f"total time = {t_1 - t_0}")