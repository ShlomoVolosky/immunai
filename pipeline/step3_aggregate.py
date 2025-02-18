"""
Goal: Validate hypothesis across all processed experiments.
1. Read all results from step2_output dir,
2. Calculate how many have "hypothesis_is_valid == True".
3. Print (true_count / total_count) * 100.
"""

import os
from .common import read_json_file

def aggregate_and_print_results(directory):
    """
    Read all experiment results from step 2,
    Calculate hoy many times the hypothesis is valid,
    Prints the Result.
    """

    all_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    if not all_files:
        print("[Step 3] No results to aggregate.")
        return

    total_count = 0
    true_count = 0

    for filename in all_files:
        filepath = os.path.join(directory, filename)
        data = read_json_file(filepath)
        if data.get("hypothesis_is_valid") is True:
            true_count += 1
        total_count += 1

    accuracy = (true_count / total_count) * 100
    print(f"[Step 3] Hypothesis is true for: {accuracy:.2f}% of processed experiments.")