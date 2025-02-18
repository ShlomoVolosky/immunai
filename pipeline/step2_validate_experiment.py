"""
Goals:
1. Read filtered data from step1_output dir.
2. Compute whether the hypothesis is TRUE or FALSE.
3. Save the result to step2_output/[EXPERIMENT_ID].json
"""
import os
from statistics import mean
from .common import read_json_file, write_json_file, get_experiment_id_from_path

def validate_hypothesis_per_experiment(input_filepath, output_dir):
    experiment_id = get_experiment_id_from_path(input_filepath)
    data = read_json_file(input_filepath) # This is the filtered data from Step 1

    neuron_in_vivo_responses = []
    non_neuron_in_vivo_responses = []

    for entry in data:
        if entry["environment"] == "In vivo":
            if entry["cell_type"] == "Neuron":
                neuron_in_vivo_responses.append(entry["cell_response"])
            else:
                non_neuron_in_vivo_responses.append(entry["cell_response"])

    # If no data or no comparison group ==> logic "cannot determine"
    if not neuron_in_vivo_responses or not non_neuron_in_vivo_responses:
        hypothesis_is_valid = False
    else:
        mean_neuron = mean(neuron_in_vivo_responses)
        mean_others = mean(non_neuron_in_vivo_responses)
        hypothesis_is_valid = (mean_neuron > mean_others)

    result = {
        "experiment_id": experiment_id,
        "hypothesis_is_valid": hypothesis_is_valid
    }

    output_filepath = os.path.join(output_dir, f"{experiment_id}.json")
    write_json_file(output_filepath, result)

    print(f"[Step 2] Experiment {experiment_id} hypothesis validation: {hypotheis_is_valid}")
    return output_filepath
