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

    kwargs_normal_range = {'min_value': 0, 'max_value': 10000}
    kwargs_large_range = {'min_value': 10000000, 'max_value': 10010000}
    kwargs_neg_range = {'min_value': -10000, 'max_value': 10000}
    kwargs_small_float = {'min_value': 0, 'max_value': 0.0001}

    # Set types based on mode
    if args.mode == 'basic':
        types = ['integer', 'float', 'word']
        type_names = ['Int-0:10000', 'Float-0:10000', 'English']
        
        gen_kwargs = [kwargs_normal_range, kwargs_normal_range, {}]
    elif args.mode == 'advanced':
        types = ['integer', 'integer', 'float', 'float', 'float',
                 'string', 'string', 'string', 'prefix_word', 'number_string']
        type_names = ['Integers-10000000:10010000',
                      'Int-n10000:10000',
                      'Float-10000000:10010000',
                      'Float-0:0.0001',
                      'Float-n10000-10000',
                      'ascii',
                      'ASCII',
                      'AsCiI',
                      'PrfxEnglish',
                      'NumberWords']
        print(len(types))
        print(len(type_names))
        gen_kwargs = [kwargs_large_range, kwargs_neg_range, kwargs_large_range, kwargs_small_float, kwargs_neg_range, {}, {}, {}, {}, {}]
        
                      
    else:
        raise ValueError("Mode must be 'basic' or 'advanced'")

    # Sizes are fixed for now
    sizes = [int(math.pow(2, i)) for i in range(1, 11)]

    # Configure name
    name = args.name+'_'+args.mode

    # Generate benchmark data
    data_utils.generate_benchmark_data(path=args.path, name=name, version=args.version, num_lists=args.num_samples, sizes=sizes, types=types, type_names=type_names, gen_kwargs=gen_kwargs)

if __name__ == "__main__":
    main()