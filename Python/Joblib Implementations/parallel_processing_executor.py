import multiprocessing
from functools import partial
import time
from tqdm import tqdm

def delayed(func):
    def wrapper(*args, **kwargs):
        return partial(func, *args, **kwargs)
    return wrapper

def _run_task(task_to_execute):
    return task_to_execute()

def simulate_work(item_id, duration):
    time.sleep(duration)
    return item_id * item_id

class ParallelExecutor:
    def __init__(self, n_jobs=-1):
        total_cores = multiprocessing.cpu_count()
        if n_jobs < 0:
            self.worker_count = total_cores + 1 + n_jobs
        else:
            self.worker_count = min(n_jobs, total_cores)
        self.process_pool = None

    def __enter__(self):
        self.process_pool = multiprocessing.Pool(self.worker_count)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process_pool.close()
        self.process_pool.join()
        self.process_pool = None

    def __call__(self, tasks):
        if self.process_pool is None:
            raise RuntimeError("Executor must be used within a 'with' statement.")
        
        return self.process_pool.map(_run_task, tasks)

if __name__ == '__main__':
    job_tasks = [delayed(simulate_work)(i, 0.1) for i in range(100)]

    print("Starting parallel execution with a progress bar...")
    start_time = time.time()
    with ParallelExecutor(n_jobs=4) as executor:
        results = executor(tqdm(job_tasks))
    end_time = time.time()
    
    print(f"\nFinal Results: {results}")
    print(f"Completed in {end_time - start_time:.4f} seconds.")