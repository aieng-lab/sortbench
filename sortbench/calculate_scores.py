import argparse

import pandas as pd

import util.result_utils as result_utils
import util.eval_utils as eval_utils


def main():
    parser = argparse.ArgumentParser(description="Generate benchmark data.")
    parser.add_argument('--csv_file', type=str, default="benchmark_results.csv", help='Path to the CSV file containing the benchmark results (default: benchmark_results.csv)')
    parser.add_argument('--result_path', type=str, default="benchmark_results", help='Path to the folder where the results files will be written (default: benchmark_results)')
    parser.add_argument('--name', type=str, default="sortbench", help='Name of the benchmark data (default: sortbench)')
    parser.add_argument('--mode', type=str, default="basic", help='Mode for the benchmark data, i.e., basic or advanced (default: basic)')
    parser.add_argument('--version', type=str, default="v1.0", help='Version of the benchmark data (default: v1.0)')

    args = parser.parse_args()

    config_names = result_utils.fetch_configs_from_results(file_path=args.result_path, name=args.name, mode=args.mode, version=args.version)
    df_results = None
    for config in config_names:
        cur_results = result_utils.load_single_result_from_disk(config, file_path=args.result_path)
        cur_df_results = eval_utils.evaluate_results(cur_results)
        if df_results is None:
            df_results = cur_df_results
        else:
            df_results = pd.concat([df_results, cur_df_results])
    df_results.to_csv(args.csv_file, index=False)


if __name__ == "__main__":
    main()
