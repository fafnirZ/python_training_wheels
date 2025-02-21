"""
The hypothesis of this implementation is that
it should take as long as the longest time.sleep in 
each batch to complete...

hypothesis proven:
took 30 seconds to complete.
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

        while job_queue:
            futures = []
            for _ in range(n_threads):
                if len(job_queue) == 0:
                    break

                _kwargs = job_queue.pop()
                futures.append(
                    executor.submit(
                        worker,
                        results,
                        **_kwargs,
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