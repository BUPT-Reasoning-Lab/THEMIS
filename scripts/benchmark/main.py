import os 
import sys
# You can import different Configs here
from basic.basic_config import *
# from CoT.CoT_config import *
from chat_engine import *

MAX_WORKERS = 2

def process_single_task(task, evaluation, position):
    """
    sample_rate：Dict | str
    inference_func：Dict | str
    Others refer to
    ```python
    from chat_engine import Processor
    ```
    """
    try:
        kwargs: dict = TASK_TYPE_PARAMS[evaluation].copy()
        if "sample_rate" in task:
            if isinstance(task["sample_rate"], dict):
                kwargs["sample_rate"] = task["sample_rate"].get(evaluation, 0)
            else:
                kwargs["sample_rate"] = task["sample_rate"]

        if "inference_func" in task:
            if isinstance(task["inference_func"], dict):
                kwargs["inference_func"] = task["inference_func"][evaluation]
            else:
                kwargs["inference_func"] = task["inference_func"]
        cleaned_keys = [k.strip("'\"") for k in task.keys()]
        if evaluation in cleaned_keys:
            for key, value in task[evaluation].items():
                if key in kwargs and key not in ["sample_rate", "task_list"]:
                    kwargs[key] = value
                    
        kwargs["namespace"] = task["namespace"]
        kwargs["tqdm_position"] = position

        processor = Processor(**kwargs)
        
        processor.run()

        print(processor.namespace,processor.task_name,"Unprocessed images:", len(processor.fetch_images()))

        return True, f"{task.get('namespace', 'unknown')} - {evaluation} "
    except Exception as e:
        import traceback

        print(e)
        return (
            False,
            f"{task.get('namespace', 'unknown')} - {evaluation} 1: {str(e)}\n{traceback.format_exc()}",
        )


from concurrent.futures import ThreadPoolExecutor, as_completed

print(f"Starting parallel execution with {MAX_WORKERS} workers...")

tasks_with_position = []
position = 0
for task in TASK_LIST:
    for evaluation in task.get("task_list", []):
        tasks_with_position.append((task, evaluation, position))
        position += 1

print(f"Total {len(tasks_with_position)} tasks to run")
print("\n" * (len(tasks_with_position) + 2)) 

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(process_single_task, task, evaluation, pos): (
            task,
            evaluation,
            pos,
        )
        for task, evaluation, pos in tasks_with_position
    }

    for future in as_completed(futures):
        task, evaluation, pos = futures[future]
        success, msg = future.result()
        status = "✓" if success else "✗"
        print(f"\n{status} {msg}")
