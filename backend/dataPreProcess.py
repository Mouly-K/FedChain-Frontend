from torch.utils.data import DataLoader,TensorDataset
from torch.utils.data import SubsetRandomSampler
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
# from imblearn.over_sampling import SMOTE
import torch
from dataclasses import dataclass,asdict
import json
import pickle
import math
@dataclass
class Dataset:
    """
    Contains all dataset related data.
    """
    train: DataLoader
    test: DataLoader
    num_train_data: int
    num_features: int
    num_labels: int
    
    def to_dict(self):
        return {
            "num_train_data": self.num_train_data,
            "num_features": self.num_features,
            "num_labels": self.num_labels,
            'train': [asdict(sample) for sample, _ in self.train],
            'test' : [asdict(sample) for sample, _ in self.test]
        }
    def to_json(self):
        return json.dumps(self.to_dict())
    def serialize(self):
        return  pickle.dumps(self.to_dict())

def PreProcess(path):
   
    X, Y = split_dataset(path)
    # Encode categorical data
    categorical_features = [i for i, e in enumerate(X[0]) if isinstance(e, str)]
    column_transformer = ColumnTransformer([("categorical", OneHotEncoder(), categorical_features)], remainder="passthrough")
    X = column_transformer.fit_transform(X)
    
    # Handle categorical class data
    y_transformer = LabelEncoder()
    Y = y_transformer.fit_transform(Y)
    
    # Scale features
    x_scaler = StandardScaler(with_mean=False, with_std=False)
    X = x_scaler.fit_transform(X)
    
    # Apply SMOTE to balance the dataset
    # smote = SMOTE(random_state=0)
    # X, Y = smote.fit_resample(X, Y)
    
    return X, Y

def split_dataset(path):
    dataset = pd.read_csv(path)
    X = dataset.iloc[:, :-1].values
    Y = dataset.iloc[:, -1].values
    return X , Y

def load_dataset(trainfile,testfile, BATCH_SIZE):
   
    X_train, Y_train = split_dataset(trainfile)
    X_test, Y_test = split_dataset(testfile)
    num_train_data = X_train.shape[0]
    num_features = X_train.shape[1]
    num_labels = 2

    train_dataset = TensorDataset(
            torch.tensor(X_train, dtype=torch.float64),
            torch.tensor(Y_train, dtype=torch.float64))
    test_dataset = TensorDataset(
            torch.tensor(X_test, dtype=torch.float64),
            torch.tensor(Y_test, dtype=torch.float64))
    
    # trainData = split_data_per(train_dataset, percentage, BATCH_SIZE)
    trainData = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=False)
    testData = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    return Dataset(train=trainData, test=testData, num_train_data=num_train_data, num_features=num_features, num_labels=num_labels)



def split_data_per(dataset, Percentage, BATCH_SIZE):
        
    chunk_size = math.floor( len(dataset) * (Percentage / 100))
    print(chunk_size)
    remaining = np.arange(len(dataset))
    indices = np.random.choice(remaining, chunk_size , replace=False)
    sampler = SubsetRandomSampler(indices)
    dataloaders = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False, sampler=sampler)
    remaining = list(set(remaining) - set(indices))
    print(len(dataloaders.dataset))
    return dataloaders

def split_data_equal(dataset, groups, BATCH_SIZE):
    """
    Split the given dataset to the given number of equal parts.
    Returns a list of dataloaders.
    """
    chunk_size = len(dataset) // groups
    # group_indices = []
    dataloaders = []
    remaining = np.arange(len(dataset))
    for i in range(groups):
        indices = np.random.choice(remaining, chunk_size, replace=False)
        sampler = SubsetRandomSampler(indices)
        dataloaders.append(DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False, sampler=sampler))
        remaining = list(set(remaining) - set(indices))
    return dataloaders