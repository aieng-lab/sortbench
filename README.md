# SortBench

SortBench is a sorting-based benchmark for Large Language Models (LLMs).

## Reproducing the benchmark

In the following we describe the steps to reproduce our results. Everything we describe works as is on Ubuntu 24.04 LTS. 

### Setting up the environment

First, checkout the repository from GitHub:

```bash
git clone git@github.com:aieng-lab/sortbench.git
cd sortbench
```

We recommend using a virtual environment to run the benchmark. To create a virtual environment, run the following command:

```bash
python3 -m venv .venv
```

We can now activate the virtual environment and install the required packages:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Creating data

To create the data, run the following command:

```bash
python sortbench/generate_data.py --mode=basic --version=v1.0 --random_seed=42415
python sortbench/generate_data.py --mode=advanced --version=v1.0 --random_seed=56671
python sortbench/generate_data.py --mode=debug --version=v1.0 --random_seed=56671
```

For reproducibiliy, each version of the benchmark uses a different, random but fixed seed. Note that different platforms (e.g., operating systems, python version, or CPUs) may yield different results, even if the seed is fixed. You can find the seeds we used below. 

| Version | Basic Seed | Advanced Seed | Debug Seed |
| ------- | ---------- | ------------- | ---------- |
| v1.0    | 42415      | 56671         | 19837      |

### Running the benchmark

To run the benchmark, you need to have valid API keys for the inference endpoints. Currently, we use models from OpenAI and models we host locally in Passau at an inference endpoint in the Inncube cluster. For both, the API keys are required. You can set them as environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export INNCUBE_API_KEY="your_inncube_api_key"
```

To run the benchmark, run the following command:

```bash
python sortbench/create_results.py --mode=basic --version=v1.0 --model_names gpt-4o gpt-4o-mini
python sortbench/create_results.py --mode=advanced --version=v1.0 --model_names gpt-4o gpt-4o-mini
python sortbench/create_results.py --mode=debug --version=v1.0 --model_names gpt-4o gpt-4o-mini
```

### Evaluating the results

To evaluate the results, run the following command:

```bash
python sortbench/calculate_scores.py --mode=basic --version=v1.0 --csv_file="scores/scores_basic_v1.0.csv"
python sortbench/calculate_scores.py --mode=advanced --version=v1.0 --csv_file="scores/scores_basic_v1.0.csv"
python sortbench/calculate_scores.py --mode=debug --version=v1.0 --csv_file="scores/scores_basic_v1.0.csv"
```

## Running the Notebooks

To use the Jupyter Notebooks we provide in the `notebooks` folder, you need to install additional dependencies. They are provided in the `notebooks/requirements.txt` file. You can install them in the same virtual environment as above (needs to be activated!) as follows:

```bash
pip install -r notebooks/requirements.txt
```

Afterwards, you can run the Jupyter Notebook server by running the following command:

```bash
jupyter notebook
```
