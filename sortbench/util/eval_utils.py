import re
import pandas as pd
from collections import Counter

def count_unordered_pairs(lst):
    """
    Count the number of unordered pairs in a list.
    
    Parameters:
    - lst (list): A list of integers.

    Returns:
    - int: The number of unordered pairs in the list.
    """
    count = 0
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                count += 1
    return count

def count_unordered_neighbors(lst):
    """
    Count the number of unordered neighbors in a list.

    Parameters:
    - lst (list): A list of integers.

    Returns:
    - int: The number of unordered neighbors in the list.
    """
    count = 0
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            count += 1
    return count

def count_missing_items(unsorted_list, sorted_list):
    """
    Count the number of missing items in the sorted list compared to the unsorted list.

    Parameters:
    - unsorted_list (list): A list of items.
    - sorted_list (list): A sorted version of the unsorted list

    Returns:
    - int: The number of missing items in the sorted list compared to the unsorted list.
    """
    unsorted_counter = Counter(unsorted_list)
    sorted_counter = Counter(sorted_list)
    missing_items = unsorted_counter - sorted_counter
    return sum(missing_items.values())

def count_additional_items(unsorted_list, sorted_list):
    """
    Count the number of additional items in the sorted list compared to the unsorted list.

    Parameters:
    - unsorted_list (list): A list of items.
    - sorted_list (list): A sorted version of the unsorted list

    Returns:
    - int: The number of additional items in the sorted list compared to the unsorted list.
    """
    unsorted_counter = Counter(unsorted_list)
    sorted_counter = Counter(sorted_list)
    additional_items = sorted_counter - unsorted_counter
    return sum(additional_items.values())

def eval_str_list(str_list):
    """
    Tries to parse a list given as a string. If the string is not valid python, we try to things:
    1. We check if the string ends in a closing bracket. If not, we look for the last comma, crop the string there and add a new closing bracket.
    2. We remove all single quotes that are not part of a string (i.e. not followed by a space or a comma) and try to evaluate the string again.

    Parameters:
    - str_list (str): A string representation of a list.

    Returns:
    - sorted_list (list): The evaluated list. None if not possible.
    - is_cropped (bool): True if the string was cropped.
    - is_cleaned (bool): True if the string was cleaned.
    """
    is_cropped = False
    is_cleaned = False
    sorted_list = None
    try:
        sorted_list = eval(str_list)
    except:
        if str_list[-1] != ']':
            cropped_sorted_list = str_list[:str_list.rfind(',')] + ']'
            is_cropped = True
        else:
            cropped_sorted_list = str_list # no cropping
        try:
            sorted_list = eval(cropped_sorted_list)
        except:
            cleaned_quote_list = re.sub("[a-zA-Z](?<!\')\'(?! |,)", "", cropped_sorted_list)
            cleaned_quote_list = cleaned_quote_list[:-1] + "']"
            is_cleaned = True
            try:
                sorted_list = eval(cleaned_quote_list)
            except:
                print('Error: Could not evaluate the cropped sorted list, not valid python')
                print(cleaned_quote_list)
    return (sorted_list, is_cropped, is_cleaned)
    

def evaluate_results(results):
    """
    Evaluate the results of the sorting benchmarks.

    Parameters:
    - results (dict): The results of the sorting benchmarks.

    Returns:
    - df_results (pd.DataFrame): A DataFrame with the evaluated results.
    """
    results_with_eval = []
    for config_name, config_data in results.items():
        benchmark_name = config_name.split('_')[0]
        benchmark_mode = config_name.split('_')[1]
        benchmark_version = config_name.split('_')[2]
        data_type = config_name.split('_')[3]
        list_length = int(config_name.split('_')[4].split('.')[0])
        
        unsorted_lists = config_data['unsorted_lists']
        
        for cur_result in config_data['results']:
            model = cur_result['model']
            for list_name, sorted_list in cur_result['sorted_lists'].items():
                sorted_list, is_cropped, is_cleaned = eval_str_list(sorted_list)

            unsorted_list = unsorted_lists[list_name]
            unordered_pairs_before = count_unordered_pairs(unsorted_list)
            unordered_pairs_after = count_unordered_pairs(sorted_list)
            unordered_neighbors_before = count_unordered_neighbors(unsorted_list)
            unordered_neighbors_after = count_unordered_neighbors(sorted_list)
            count_missing = count_missing_items(unsorted_list, sorted_list)
            count_additional = count_additional_items(unsorted_list, sorted_list)
            len_diff = len(unsorted_list)-len(sorted_list)
            #print(cur_result)
            #print(config_data)
   
            results_with_eval.append({
                'Benchmark': benchmark_name,
                'Mode': benchmark_mode,
                'Version': benchmark_version,
                'Model': model,
                'Type': data_type,
                'Size': list_length,
                'Unordered Pairs Before': unordered_pairs_before,
                'Unordered Pairs After': unordered_pairs_after,
                'Unordered Neighbors Before': unordered_neighbors_before,
                'Unordered Neighbors After': unordered_neighbors_after,
                'Missing Items': count_missing,
                'Additional Items': count_additional,
                'Length Difference': len_diff,
                'Cropped': is_cropped,
                'Cleaned': is_cleaned
            })
    
    df_results = pd.DataFrame(results_with_eval)
    return df_results
