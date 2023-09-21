import torch.nn as nn
import torch.nn.functional as F
import torch
from FederatedLearning import FederatedModel
class AutoencoderWithClassifier(FederatedModel):
    def __init__(self, input_size, num_classes ):
        super().__init__()
        self.MODEL_NAME = "AutoEncoder"
        self.encoding_size = 32
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(True),
            nn.Linear(64, 32),
            nn.ReLU(True),
            nn.Linear(32, self.encoding_size),
        )
        self.classifier = nn.Sequential(
            nn.Linear(self.encoding_size, 16),
            nn.ReLU(True),
            nn.Linear(16, num_classes)
        )
        self.decoder = nn.Sequential(
            nn.Linear(self.encoding_size, 32),
            nn.ReLU(True),
            nn.Linear(32, 64),
            nn.ReLU(True),
            nn.Linear(64, input_size),
            nn.Sigmoid()
        )
        self.model = nn.Sequential(self.encoder, self.classifier, self.decoder)

    def forward(self, x):
        x_encoded = self.model[0](x)
        x_classify = self.model[1](x_encoded)
        x_decoded = self.model[2](x_encoded)
        return x_classify





class LSTMModel(FederatedModel):
    def __init__(self, num_features,num_labels):
        super().__init__()
        self.MODEL_NAME = "LSTMModel"
        hidden_size = 64  # Number of features in the hidden state
        num_layers = 2  # Number of LSTM layers
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.model = nn.Sequential(
            nn.LSTM(num_features, hidden_size, num_layers,batch_first=True),
            nn.Linear(hidden_size, num_labels)
        )

    def forward(self, x):
        x = x.view(-1, 1, x.shape[1])
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size,dtype = x.dtype).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size ,dtype =x.dtype).to(x.device)
        
        out, _ = self.model[0](x, (h0, c0))
        out = self.model[1](out[:, -1, :])
        return out

class SingleLayer(FederatedModel):
    
    def __init__(self, num_features, num_labels):
        super().__init__()
        n = 5
        self.fc1 = nn.Linear(num_features, n)
        self.fc2 = nn.Linear(n, num_labels)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class DBN(FederatedModel):
    def __init__(self, num_features, num_labels):
        super().__init__()
        self.MODEL_NAME = "DBN"
        self.num_layers = 3
        self.layers = nn.ModuleList()
        neuron_counts = [100, 150, 200]
        # Create the input layer
        self.layers.append(nn.Linear(num_features, neuron_counts[0]))
        self.layers.append(nn.Sigmoid())

        # Create the hidden layers
        for i in range(1, self.num_layers):
            self.layers.append(nn.Linear(neuron_counts[i - 1], neuron_counts[i]))
            self.layers.append(nn.Sigmoid())

        # Create the output layer
        self.layers.append(nn.Linear(neuron_counts[-1], num_labels))

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x



