# SortBench

SortBench is a sorting-based benchmark for Large Language Models (LLMs).

## Creating data

To create the data, run the following command:

```bash
python sortbench/generate_data.py --mode=basic --version=v1.0 --random_seed=1
python sortbench/generate_data.py --mode=advanced --version=v1.0 --random_seed=1
```

We decided to use the main version number of random seed to enable reproducibility. Note that different platforms (e.g., operating systems, python version, or CPUs) may yield different results, even if the seed is fixed.

## Running the benchmark

To run the benchmark, run the following command:

```bash
python sortbench/create_results.py --mode=basic --version=v1.0 --model_names gpt-4o gpt-4o-mini
python sortbench/create_results.py --mode=advanced --version=v1.0 --model_names gpt-4o gpt-4o-mini
```
