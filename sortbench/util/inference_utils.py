import os
import time
import traceback

from util.result_utils import check_if_result_available

from openai import OpenAI, InternalServerError
import anthropic

_OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
_INNCUBE_MODELS = ["llama3.1", "gemma2", "qwen2.5", "deepseekr1"]
_ANTROPIC_MODELS = ["claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022"]

def is_model_supported(model):
    """
    Check if a model is supported by sortbench.
    
    Parameters:
    - model (str): the model name
    """
    return model in _OPENAI_MODELS+_INNCUBE_MODELS+_ANTROPIC_MODELS

def sort_list_with_antropic_api(unsorted_list, api_key, model, system_prompt=None, prompt=None):
    """
    Calls the Antropic API to sort a list.

    Parameters:
    - unsorted_list (list): the list to be sorted
    - api_key (str): the Antropic API key
    - model (str): the model to use for inference
    - system_prompt (str): the system prompt to use
    - prompt (str): the prompt to use
    """
    
    if system_prompt is None:
        system_prompt = "Your task is to sort a list according to the common sorting of the used data type in Python. The output must only contain the sorted list and nothing else. The format of the list must stay the same."
    if prompt is None:
        prompt = f"Sort the following list: {unsorted_list}"
    else:
        print('not yet implemented')
        return None
    
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=1,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    sorted_list = message.content[0].text
    return sorted_list


def sort_list_with_openai_api(unsorted_list, api_key, model, url=None, use_streaming=False, system_prompt=None, prompt=None, max_attempts=1):
    """
    Calls the OpenAI API to sort a list.

    Parameters:
    - unsorted_list (list): the list to be sorted
    - api_key (str): the OpenAI API key
    - model (str): the model to use for inference
    - url (str): the URL of the OpenAI API endpoint
    - system_prompt (str): the system prompt to use
    - prompt (str): the prompt to use
    - max_attempts (int): the maximum number of attempts to make
    """

    # setup system prompt and prompt
    if system_prompt is None:
        system_prompt = "Your task is to sort a list according to the common sorting of the used data type in Python. The output must only contain the sorted list and nothing else. The format of the list must stay the same."
    if prompt is None:
        prompt = f"Sort the following list: {unsorted_list}"
    else:
        print('not yet implemented')
        return None
    
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        if url is None:
            client = OpenAI(api_key=api_key)
        else:
            client = OpenAI(api_key=api_key, base_url=url)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=use_streaming
            )
            if use_streaming:
                # uncomment collected chunks for debugging
                # collected_chunks = []
                collected_messages = []
                for chunk in response:
                    # collected_chunks.append(chunk)
                    chunk_message = chunk.choices[0].delta.content
                    collected_messages.append(chunk_message)
                #finish_reason = response.choices[0].finish_reason
                #if finish_reason != 'stop':
                #    raise RuntimeError(f"Stream did not finish properly: {finish_reason}")
                sorted_list = ''.join([m for m in collected_messages if m is not None])
            else:
                sorted_list = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Exception running inference: {e}")
            print()
            print(unsorted_list)
            if attempts == max_attempts:
                print("Waiting 60 seconds before next sequence...")
                time.sleep(60)
                raise RuntimeError()
            else:
                print("Waiting 60 seconds before next attempt...")
                time.sleep(60)
        finally:
            client.close()
    
    return sorted_list

def run_single_config_for_model(config_name, lists, model="gpt-4o-mini", verbose=True, results=None):
    """
    Run inference on all configs for a single model.

    Parameters:
    - configs (dict): the dictionary of configs
    - api_key (str): the OpenAI API key
    - model (str): the model to use for inference
    - verbose (bool): whether to print verbose output
    - results (dict): the dictionary of results that already exist to avoid re-running inference
    """

    if results is None:
        results = {}
        
    cur_results = {}
    cur_results['model'] = model
    cur_results['sorted_lists'] = {}
    
    try:
        for unsorted_list_name, unsorted_list in lists.items():
            if verbose:
                print(f"Sorting list {unsorted_list_name} using model {model} for config {config_name}")
            if model in _OPENAI_MODELS:
                api_key = os.getenv("OPENAI_API_KEY")
                sorted_list = sort_list_with_openai_api(unsorted_list, api_key, model=model)
            elif model in _INNCUBE_MODELS:
                api_key = os.getenv("INNCUBE_API_KEY")
                endpoint_url = "https://llms-inference.innkube.fim.uni-passau.de"
                sorted_list = sort_list_with_openai_api(unsorted_list, api_key, model=model, url=endpoint_url, use_streaming=True, max_attempts=2)
            elif model in _ANTROPIC_MODELS:
                api_key = os.getenv("ANTROPIC_API_KEY")
                sorted_list = sort_list_with_antropic_api(unsorted_list, api_key, model=model)
            else:
                raise ValueError(f"Model {model} not supported")
            cur_results['sorted_lists'][unsorted_list_name] = sorted_list

        if config_name in results:
            results[config_name]['results'].append(cur_results)
        else:
            results[config_name] = {'unsorted_lists': lists,
                                    'results': [cur_results]}
    except Exception as e:
        print(f"Error while running inference for config {config_name} and model {model}: {e}")
        print(traceback.format_exc())

    return results


def run_configs_for_single_model(configs, model="gpt-4o-mini", verbose=True, results=None):
    """
    Run inference on all configs for a single model.

    Parameters:
    - configs (dict): the dictionary of configs
    - api_key (str): the OpenAI API key
    - model (str): the model to use for inference
    - verbose (bool): whether to print verbose output
    - results (dict): the dictionary of results that already exist to avoid re-running inference
    """
    if not is_model_supported(model):
        raise ValueError(f"Model {model} not supported")

    if results is None:
        results = {}    
    for config_name, lists in configs.items():
        if check_if_result_available(results, config_name, model):
            if verbose:
                print(f"Results for config {config_name} and model {model} already available. Skipping.")
            continue
        cur_results = {}
        cur_results['model'] = model
        cur_results['sorted_lists'] = {}
        
        try:
            for unsorted_list_name, unsorted_list in lists.items():
                if verbose:
                    print(f"Sorting list {unsorted_list_name} using model {model} for config {config_name}")
                if model in _OPENAI_MODELS:
                    api_key = os.getenv("OPENAI_API_KEY")
                    sorted_list = sort_list_with_openai_api(unsorted_list, api_key, model=model)
                elif model in _INNCUBE_MODELS:
                    api_key = os.getenv("INNCUBE_API_KEY")
                    endpoint_url = "https://llms-inference.innkube.fim.uni-passau.de"
                    sorted_list = sort_list_with_openai_api(unsorted_list, api_key, model=model, url=endpoint_url, use_streaming=True, max_attempts=2)
                elif model in _ANTROPIC_MODELS:
                    api_key = os.getenv("ANTROPIC_API_KEY")
                    sorted_list = sort_list_with_antropic_api(unsorted_list, api_key, model=model)
                else:
                    raise ValueError(f"Model {model} not supported")
                cur_results['sorted_lists'][unsorted_list_name] = sorted_list
        
            results[config_name] = {'unsorted_lists': lists,
                                    'results': [cur_results]}
        except Exception as e:
            print(f"Error while running inference for config {config_name} and model {model}: {e}")
            print(traceback.format_exc())

    return results
