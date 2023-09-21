import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from dataPreProcess import PreProcess
from config import config
def split_and_save_balanced_datasets(path, num_splits, random_state=None,test_size =0.2):
    """
    Split the dataset into train and test sets, then split the training set into balanced parts
    and save them as CSV files.

    Args:
        X (numpy.ndarray or pandas.DataFrame): Input features.
        y (numpy.ndarray or pandas.Series): Target variable.
        test_size (float): Proportion of the dataset to include in the test split.
        num_splits (int): Number of balanced parts to split the training set into.
        output_dir (str): Path to the output directory where CSV files will be saved.
        random_state (int or None, optional): Random state for reproducibility.

    Returns:
        tuple: A tuple containing the test set (X_test, y_test) and the balanced splits of the training set.
    """
    # Split the dataset into train and test sets
    X, Y = PreProcess(path)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)

    # Split the training set into balanced parts
    balanced_splits = split_dataset_stratified(X_train, y_train, num_splits, random_state)

    # Create the output directory if it doesn't exist
    X_columns = [f"Feature_{i}" for i in range(X.shape[1])]
    # Save the balanced splits as CSV files
    for i, (train_data, train_labels, _, _) in enumerate(balanced_splits):
        # Create a DataFrame with the train data and labels
        df = pd.DataFrame(np.column_stack((train_data, train_labels)), columns=[*X_columns, 'label'])

        # Save the DataFrame to a CSV file
        filename = f"data{i+1}.csv"
        output_path = os.path.join(config.Train, filename)
        df.to_csv(output_path, index=False)
    test_data = pd.DataFrame(np.column_stack((X_test, y_test)), columns=[*X_columns, 'label'])
    test_data.to_csv(config.Test, index=False)
    

def split_dataset_stratified(X, y, num_splits, random_state=None):
    """
    Split the dataset into balanced parts while preserving the class distribution.

    Args:
        X (numpy.ndarray or pandas.DataFrame): Input features.
        y (numpy.ndarray or pandas.Series): Target variable.
        num_splits (int): Number of balanced parts to split the dataset into.
        random_state (int or None, optional): Random state for reproducibility.

    Returns:
        list: A list of tuples, where each tuple contains a subset of the original dataset
              and the corresponding labels.
    """
    # Convert dataset and labels to numpy arrays
    X = np.array(X)
    y = np.array(y)

    # Create a stratified split generator
    sss = StratifiedShuffleSplit(n_splits=num_splits, test_size=1/num_splits, random_state=random_state)

    # Split the dataset into balanced parts
    splits = []
    for train_index, test_index in sss.split(X, y):
        train_data = X[train_index]
        train_labels = y[train_index]
        test_data = X[test_index]
        test_labels = y[test_index]
        splits.append((train_data, train_labels, test_data, test_labels))

    return splits

split_and_save_balanced_datasets(config.DatasetPath, config.NUM_DATA, random_state=42,test_size = config.TEST_SIZE)