import json
import os

def load_results_from_disk(file_path='benchmark_results'):
    """
    Load all results from a local directory into a dict of dicts. Will return an empty dict if no results are found.

    Parameters:
    file_path (str): path to directory containing results files (default: 'benchmark_results')
    """
    results = {}
    for filename in os.listdir(file_path):
        with open(os.path.join(file_path, filename), 'r') as f:
            data = json.load(f)
            results[filename] = data
    return results

def check_if_result_available(results, config_name, model_name):
    """
    Check if results for a specific config and model are already available.

    Parameters:
    results (dict): dict containing all results
    config_name (str): name of the config
    model_name (str): name of the model
    """
    if config_name in results:
        model_names = [result['model'] for result in results[config_name]['results']]
        if model_name in model_names:
            return True
    return False

def write_results_to_disk(results, file_path='benchmark_results', overwrite=False):
    """
    Write results to disk.

    Parameters:
    results (dict): dict containing all results
    file_path (str): path to directory to write results files to (default: 'benchmark_results')
    overwrite (bool): whether to overwrite existing files or whether to append new results (default: False)
    """
    for config_name, config_results in results.items():
        file = os.path.join(file_path, config_name)
        os.makedirs(os.path.dirname(file), exist_ok=True)
        if not overwrite and os.path.exists(file):
            # read existing results and update
            with open(file, 'r') as f:
                existing_results = json.load(f)
                existing_results['results'] = existing_results['results'] + config_results['results']
                dict_to_write = existing_results
        else:
            dict_to_write = config_results

        with open(file, 'w') as f:
            json.dump(dict_to_write, f)
