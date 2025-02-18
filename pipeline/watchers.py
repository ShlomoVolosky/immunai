"""
WatchDog:
Watch Directories and Trigger Steps:
1. A watch on raw_experiment_data/ to trigger step1_extract.py,
2. A watch on step1_output/ to trigger step2_validate_experiment.py,
3. A watch on step2_output/ to trigger step3_aggregate.py.
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .step1_extract import extract_relevant_data
from .step2_validate_experiment import validate_hypothesis_per_experiment
from .step3_aggregate import aggregate_and_print_results

RAW_DIR = "raw_experiment_data"
STEP1_OUT_DIR = "step1_output"
STEP2_OUT_DIR = "step2_output"

class RawDataHandler(FileSystemEventHandler):
    """
    Watches raw_experiment_data dir,
    Triggers step1_extract.py.
    """
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            extract_relevant_data(event.src_path, STEP1_OUT_DIR)


class Step1Handler(FileSystemEventHandler):
    """
    Watches step1_output dir,
    Triggers step2_validate_experiment.py.
    """
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            validate_hypothesis_per_experiment(event.src_path, STEP2_OUT_DIR)


class Step2Handler(FileSystemEventHandler):
    """
    Watches step2_output dir,
    Triggers step3_aggregate.py.
    """
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            # Remember: This step does not produce a file, only the aggregated result.
            aggregate_and_print_results(STEP2_OUT_DIR)

def start_watchers():
    # Creation of watchers for each directory.
    observer = Observer()

    observer.schedule(RawDataHandler(), RAW_DIR, recursive = False)
    observer.schedule(Step1Handler(), STEP1_OUT_DIR, recursive = False)
    observer.schedule(Step2Handler(), STEP2_OUT_DIR, recursive = False)

    observer.start()
    print("Watching for new files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()