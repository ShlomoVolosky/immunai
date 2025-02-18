# README

Welcome to this small data pipeline for validating a hypothesis about single cell experiments.  
The hypothesis is:

> **"Neurons have a higher response in 'In vivo' environments compared to other cell types on average."**

This repository demonstrates how we can build a simple **three‑stage** pipeline that listens for new data, processes and validates each experiment, and then aggregates the results to show how often the hypothesis holds true.

---

## 1. Why This Pipeline?

**Problem Statement:**  
We have a set of experiments, each described by a JSON file with detailed information about single cells (neuron or otherwise). For each experiment, our task is to **extract** only the relevant bits, **validate** the hypothesis, and then **summarize** how often the hypothesis is true.  

**Key Goals:**  
1. Keep the process **modular** (three distinct steps).  
2. Make the process **repeatable** and **asynchronous**: whenever a new experiment arrives, it should automatically be processed without us manually running commands.  
3. Maintain **traceability**: each step of the pipeline writes an output file or prints a result, so we can see the evolution of our data.

---

## 2. Pipeline Overview

Here's the flow:

1. **Step 1**: Extract relevant data from the raw experiment file (only the fields needed for our hypothesis).  
2. **Step 2**: Validate whether the hypothesis holds for that experiment (comparing neuron response to other cell types in 'In vivo').  
3. **Step 3**: Aggregate results across all experiments processed so far and print the overall percentage of times our hypothesis is true.

### Directory Structure

raw_experiment_data/          --> [Triggered] --> Step 1 --> step1_output/
step1_output/                 --> [Triggered] --> Step 2 --> step2_output/
step2_output/                 --> [Triggered] --> Step 3 --> Print aggregated results


Each step writes its output to a new directory, so you can keep a record of what happened at each stage.

---

## 3. Why `watchdog`?

We want a system where as soon as a new file lands in `raw_experiment_data/`, the pipeline runs **automatically**. One way to do this is to:

- **Poll** the directory with a script in an infinite loop, but that can be inefficient and messy.  
- Use **cron** or scheduled tasks, but that might still introduce intervals of waiting and is less immediate.  
- **Manually** run a script each time you add a file—which is error‑prone and not very convenient if you want a hands‑off system.

**`watchdog`** solves this nicely. It's a Python library that monitors a directory in real time. When `watchdog` sees a new file (or a file change), it triggers a function or a method of our choice. This gives us an **event-driven** approach to pipeline execution, which is smoother and more responsive than polling or manual steps.  

**In short**: I chose `watchdog` because it’s **simple**, **lightweight**, and designed exactly for this purpose—watching directories for new or changed files and letting you react immediately.

---

## 4. How It All Fits Together

Below is a quick summary of the scripts:

1. **`step1_extract.py`**  
   - Reads the newly arrived JSON in `raw_experiment_data/`.  
   - Filters the data to only the necessary fields (like cell type, environment, and cell response).  
   - Saves the filtered data to `step1_output/`.

2. **`step2_validate_experiment.py`**  
   - Reads the filtered file from `step1_output/`.  
   - Calculates whether the hypothesis ("Neuron"/"In vivo" > other cell types in "In vivo") is **true** or **false**.  
   - Writes a simple JSON with `{"experiment_id": "...", "hypothesis_valid": bool}` to `step2_output/`.

3. **`step3_aggregate.py`**  
   - Reads *all* the results in `step2_output/`.  
   - Counts how many are true vs total, calculates a percentage, then prints something like:  
     ```
     Hypothesis is true for: 66.67% of processed experiments.
     ```

4. **`watchers.py`**  
   - Uses `watchdog` to listen for new files in the three directories (`raw_experiment_data/`, `step1_output/`, `step2_output/`).  
   - Triggers the correct step whenever a new file appears.  
   - Allows the pipeline to run **automatically** and asynchronously, so multiple experiments can be processed with minimal effort.

Finally, `main.py` starts the watchers.

