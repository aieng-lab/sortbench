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
    is_list = False
    has_ellipsis = False
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
                #print('Error: Could not evaluate the cropped sorted list, not valid python')
                pass

    if type(sorted_list)==list:
        is_list = True
    else:
        if type(sorted_list)==tuple:
            if str_list.startswith('(\''):
                sorted_list = list(sorted_list)
            elif str_list.startswith('([') or str_list.endswith('],'):
                sorted_list = sorted_list[0]
            is_list = False
    if sorted_list is not None and type(sorted_list[-1])==type(...):
        sorted_list = sorted_list[:-1]
        has_ellipsis = True
            
    return (sorted_list, is_cropped, is_cleaned, is_list, has_ellipsis)
    

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
                sorted_list, is_cropped, _, is_list, has_ellipsis = eval_str_list(sorted_list)
                unsorted_list = unsorted_lists[list_name]
                if sorted_list is None:
                    unordered_pairs_before = None
                    unordered_pairs_after = None
                    unordered_neighbors_before = None
                    unordered_neighbors_after = None
                    count_missing = None
                    count_additional = None
                    len_diff = None
                    is_parsed = False
                else:
                    unordered_pairs_before = count_unordered_pairs(unsorted_list)
                    unordered_pairs_after = count_unordered_pairs(sorted_list)
                    unordered_neighbors_before = count_unordered_neighbors(unsorted_list)
                    unordered_neighbors_after = count_unordered_neighbors(sorted_list)
                    count_missing = count_missing_items(unsorted_list, sorted_list)
                    count_additional = count_additional_items(unsorted_list, sorted_list)
                    len_diff = len(unsorted_list)-len(sorted_list)
                    is_parsed = True
    
                results_with_eval.append({
                    'Benchmark': benchmark_name,
                    'Mode': benchmark_mode,
                    'Version': benchmark_version,
                    'Model': model,
                    'Type': data_type,
                    'Size': list_length,
                    'List Name': list_name,
                    'Unordered Pairs Before': unordered_pairs_before,
                    'Unordered Pairs After': unordered_pairs_after,
                    'Unordered Neighbors Before': unordered_neighbors_before,
                    'Unordered Neighbors After': unordered_neighbors_after,
                    'Missing Items': count_missing,
                    'Additional Items': count_additional,
                    'Length Difference': len_diff,
                    'Parsed': is_parsed,
                    'Cropped': is_cropped,
                    'IsList': is_list,
                    'HasEllipsis': has_ellipsis
                })
    
    df_results = pd.DataFrame(results_with_eval)
    df_results = normalize_metrics(df_results)
    df_results = compute_total_score(df_results)
    return df_results

def normalize_metrics(df_results):
    """
    Normalize the metrics to be percentages of the size of the list. In case of pairs, we normalize by the number of pairs in the list.

    Parameters:
    - df_results: DataFrame with the results of the benchmark

    Returns:
    - df_results: DataFrame with the normalized metrics
    """

    df_results['Unordered Pairs (%)'] = df_results['Unordered Pairs After']/(df_results['Size']*(df_results['Size']-1)/2)
    df_results['Unordered Neighbors (%)'] = df_results['Unordered Neighbors After']/df_results['Size']
    df_results['Missing Items (%)'] = (df_results['Missing Items']/df_results['Size']).clip(upper=1)
    df_results['Additional Items (%)'] = (df_results['Additional Items']/df_results['Size']).clip(upper=1)
    df_results['Absolute Length Difference (%)'] = abs(df_results['Length Difference']/df_results['Size'])
    return df_results

def compute_total_score(df_results):
    """
    Compute the total score for each benchmark result.

    Parameters:
    - df_results: DataFrame with the results of the benchmark

    Returns:
    - df_results: DataFrame with the total score for each benchmark result
    """
    df_results['Validity Score'] = 0.0
    df_results.loc[(df_results['Parsed']==True) & (df_results['Cropped']==True), 'Validity Score'] = 0.5
    df_results.loc[(df_results['Parsed']==True) & (df_results['Cropped']==False) & (df_results['IsList']==False), 'Validity Score'] = 0.75
    df_results.loc[(df_results['Parsed']==True) & (df_results['Cropped']==False) & (df_results['HasEllipsis']==True), 'Validity Score'] = 0.75
    df_results.loc[(df_results['Parsed']==True) & (df_results['Cropped']==False) & (df_results['IsList']==True) & (df_results['HasEllipsis']==False), 'Validity Score'] = 1.0
    df_results['Sorting Score'] = 1-(df_results['Unordered Pairs (%)'] + df_results['Unordered Neighbors (%)'])/2
    df_results['Faithfulness Score'] = 1-(df_results['Missing Items (%)'] + df_results['Additional Items (%)'])/2
    df_results['SortBench Score'] = df_results['Validity Score']*(df_results['Sorting Score'] + df_results['Faithfulness Score'])/2
    return df_results
