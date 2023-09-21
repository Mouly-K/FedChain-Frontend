
import numpy as np
import torch
import pickle

def Combined_Mean(means, size, Gmean, Gsize):
    total = np.multiply(means, size) + np.multiply(Gmean, Gsize)
    final = total / (size + Gsize)
    return final

def Combined_Std(stds, size, Gstds, Gsize):
    total = np.multiply(stds, size) + np.multiply(Gstds, Gsize)
    total_sum = (Gsize + size)
    
    epsilon = np.finfo(float).eps  # Get the smallest representable positive number
    total = np.where(total == 0, epsilon, total)
    
    total = total / total_sum
    return np.sqrt(total)


def localStatistics(dataset):
    X = torch.cat([x for x, y in dataset])
    mean = X.mean(0, keepdim=True)
    stds = (X - mean).square().mean(0, keepdim=True)
    epsilon = np.finfo(float).eps  # Get the smallest representable positive number
    stds = np.where(stds == 0, epsilon, stds)
    size = X.shape[0]
    return size,mean,stds


def save_dataset(dataset, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(dataset, f)