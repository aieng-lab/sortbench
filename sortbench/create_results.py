import argparse
import os

import util.result_utils as result_utils
import util.data_utils as data_utils
import util.inference_utils as inference_utils


def main():
    parser = argparse.ArgumentParser(description="Generate benchmark data.")
    parser.add_argument('--data_path', type=str, default="benchmark_data", help='Path to the folder where the data files will be written (default: benchmark_data)')
    parser.add_argument('--result_path', type=str, default="benchmark_results", help='Path to the folder where the results files will be written (default: benchmark_results)')
    parser.add_argument('--name', type=str, default="sortbench", help='Name of the benchmark data (default: sortbench)')
    parser.add_argument('--mode', type=str, default="basic", help='Mode for the benchmark data, i.e., basic or advanced (default: basic)')
    parser.add_argument('--version', type=str, default="v1.0", help='Version of the benchmark data (default: v1.0)')
    parser.add_argument('--model_names', nargs='+', default=["gpt-4o-mini"], help='List of model names to run inference on (default: ["gpt-4o-mini"])')

    args = parser.parse_args()
    
    # Set model names
    models = args.model_names
    for model in models:
        if not inference_utils.is_model_supported(model):
            raise ValueError(f"Model {model} is not supported by sortbench")

    # Load benchmark data and existing results
    configs = data_utils.load_data_local(file_path=args.data_path, name=args.name, mode=args.mode, version=args.version)

    for model in models:
        for config_name, lists in configs.items():
            print(f"Config: {config_name} --- Model {model}")
            if result_utils.check_if_result_available_on_disk(args.result_path, config_name, model):
                print(f"Results already available, skipping")
                continue
            print('Results not available, running inference')
            results = result_utils.load_single_result_from_disk(config_name, args.result_path)
            results = inference_utils.run_single_config_for_model(config_name, lists, model=model, results=results)
            print('Inference finished, writing results to disk')
            result_utils.write_results_to_disk(results, file_path=args.result_path, overwrite=True)
            print('Finished writing results to disk')

if __name__ == "__main__":
    main()
