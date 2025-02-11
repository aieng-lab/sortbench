import argparse
import math
import random

import util.data_utils as data_utils

def main():
    parser = argparse.ArgumentParser(description="Generate benchmark data.")
    parser.add_argument('--path', type=str, default="benchmark_data", help='Path to the folder where the data files will be written (default: benchmark_data)')
    parser.add_argument('--name', type=str, default="sortbench", help='Name of the benchmark data (default: sortbench)')
    parser.add_argument('--mode', type=str, default="basic", help='Mode for the benchmark data, i.e., basic or advanced (default: basic)')
    parser.add_argument('--version', type=str, default="v1.0", help='Version of the benchmark data (default: v1.0)')
    parser.add_argument('--random_seed', type=int, default=None, help='Random seed for data generation (default: None)')
    parser.add_argument('--num_samples', type=int, default=100, help='Number of lists to generate (default: 100)')

    args = parser.parse_args()

    # Set random seed if provided
    if args.random_seed is not None:
        if args.random_seed < 0:
            raise ValueError("Random seed must be a non-negative integer")
        random.seed(args.random_seed)

    # Set types based on mode
    if args.mode == 'basic':
        types = ['integer', 'float', 'string', 'word']
    elif args.mode == 'advanced':
        types = ['number_string', 'prefix_string', 'prefix_words']
    else:
        raise ValueError("Mode must be 'basic' or 'advanced'")

    # Sizes are fixed for now
    sizes = [int(math.pow(2, i)) for i in range(1, 11)]

    # Configure name
    name = args.name+'_'+args.mode

    # Generate benchmark data
    data_utils.generate_benchmark_data(path=args.path, name=name, version=args.version, num_lists=args.num_samples, sizes=sizes, types=types)

if __name__ == "__main__":
    main()