"""
Here we define utility functions that multiple steps might use:
For example: reading and writing JSON, logging, etc.
"""
import json
import os

def read_json_file(filepath):
    """Read JSON data from a file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def write_json_file(filepath, data):
    """Write JSON data to a file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_experiment_id_from_path(filepath):
    """
    Extract the experiment ID from a path like:
    raw_experiment_data/0001.json -> '0001'
    or step1_output/0002.json -> '0002'
    """
    filename = os.path.basename(filepath)
    experiment_id, _ = os.path.splittext(filename)
    return experiment_id