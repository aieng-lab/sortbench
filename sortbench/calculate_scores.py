import argparse

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

    # Load benchmark data and existing results
    results = result_utils.load_results_from_disk(file_path=args.result_path)
    df_results = eval_utils.evaluate_results(results)

    df_results.to_csv(args.csv_file, index=False)


if __name__ == "__main__":
    main()
