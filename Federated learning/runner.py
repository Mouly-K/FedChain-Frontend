import subprocess

datasets = ['mnist', 'fmnist', 'cifar']
models = ['mlp', 'cnn']
iid_options = [0, 1]  # 0 for non-IID, 1 for IID

# Run baseline_main.py and federated_main.py for all combinations
for dataset in datasets:
    for model in models:
        for iid in iid_options:
            print(f"Running for dataset: {dataset}, model: {model}, iid: {iid}")

            # Run baseline_main.py
            baseline_command = f"python src/baseline_main.py --dataset {dataset} --model {model}"
            subprocess.run(baseline_command, shell=True)

            # Run federated_main.py with equal option
            federated_command = f"python src/federated_main.py --dataset {dataset} --model {model} --iid {iid} --unequal=1"
            subprocess.run(federated_command, shell=True)

            # Run federated_main.py without equal option
            federated_command_no_equal = f"python src/federated_main.py --dataset {dataset} --model {model} --iid {iid}"
            subprocess.run(federated_command_no_equal, shell=True)
