import torch
import torch.nn as nn
import torch.optim as optim
import torch
import torch.nn as nn
import torch.optim as optim
from utils import Combined_Mean, Combined_Std, localStatistics
def train_model(model, train_loader, num_epochs, learning_rate, mean, standard_deviation):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    for epoch in range(num_epochs):
        # model.train()
        running_loss = 0.0
        for batch , (inputs, targets) in enumerate(train_loader):
            inputs_normalized = (inputs - mean) / standard_deviation
            
            optimizer.zero_grad()
            classifications = model(inputs_normalized.float())
            
            
            
            loss = criterion(classifications, targets.long())
            
            if torch.isnan(loss):
                print("NaN loss value. Skipping batch.")
                continue
            
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
        
        epoch_loss = running_loss / len(train_loader.dataset)
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')

# Define the evaluation function
def evaluate_model(model, test_loader,block_data=None):
    model.eval()
    correct = 0
    total = 0
    size,mean,std = localStatistics(test_loader)
    if block_data:
        mean = Combined_Mean(mean, size ,block_data['mean'],block_data['size']) 
        std = Combined_Std(std, size, block_data['std_dev'], block_data['size'])
    
    with torch.no_grad():
        for inputs, targets in test_loader:
            if block_data:
                inputs_normalized = (inputs - mean) / std
            
            classifications = model(inputs_normalized.float())
            predicted = torch.argmax(classifications, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()
    accuracy = correct / total
    return accuracy