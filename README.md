# SortBench

SortBench is a sorting-based benchmark for Large Language Models (LLMs).

## Creating data

To create the data, run the following command:

```bash
python sortbench/generate_data.py --mode=basic --version=v1.0 --random_seed=42415
python sortbench/generate_data.py --mode=advanced --version=v1.0 --random_seed=56671
```

For reproducibiliy, each version of the benchmark uses a different, random but fixed seed. Note that different platforms (e.g., operating systems, python version, or CPUs) may yield different results, even if the seed is fixed. You can find the seeds we used below. 

| Version | Basic Seed | Advanced Seed |
| ------- | ---------- | ------------- |
| v1.0    | 42415      | 56671         |

## Running the benchmark

To run the benchmark, run the following command:

```bash
python sortbench/create_results.py --mode=basic --version=v1.0 --model_names gpt-4o gpt-4o-mini
python sortbench/create_results.py --mode=advanced --version=v1.0 --model_names gpt-4o gpt-4o-mini
```

## Evaluating the results

To evaluate the results, run the following command:

```bash
python sortbench/calculate_scores.py --mode=basic --version=v1.0 --csv_file="scores/scores_basic_v1.0.csv"
python sortbench/calculate_scores.py --mode=advanced --version=v1.0 --csv_file="scores/scores_basic_v1.0.csv"
```

