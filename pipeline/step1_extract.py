"""Principle: Save only what you need.
I am keeping only: cell_type.name, environment.name and cell_response from JSON data
"""

import os
from .common import read_json_file, write_json_file, get_experiment_id_from_path

def extract_relevant_data(input_filepath, output_dir):
    """
    Extract only relevant data to assess the hypothesis, 
    then save JSON in output_dir.
    """
    experiment_id = get_experiment_id_from_path(input_filepath)
    data = read_json_file(input_filepath)

    relevant_entries = []
    for entry in data:
        filtered_entry = {
            "cell_type": entry["cell_type"]["name"],
            "environment": entry["environment"]["name"],
            "cell_response": entry["cell_response"]
        }
        relevant_entries.append(filtered_entry)

    # Write to step1_output/000n.JSON
    output_filepath = os.path.join(output_dir, f"{experiment_id}.json")
    write_json_file(output_filepath, relevant_entries)

    print(f"[Step 1] Extracted relevant data from experiment {experiment_id}")
    return output_filepath