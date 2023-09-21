import numpy as np
import torch.nn as nn

class FederatedModel(nn.Module):

    def to_bytes(self):
        """
        Returns the byte representation of the autoencoder model's parameters.
        """
        bytestr = b''
        bytestr = b''
        if self.MODEL_NAME == "DBN":
            for layer in self.layers:
                if isinstance(layer, nn.Linear):
                    for param in layer.parameters():
                        arr = param.detach().numpy().astype(np.float64)
                        bytestr += arr.tobytes()
        elif self.MODEL_NAME == "LSTMModel":
            for name, param in self.model.named_parameters():
                arr = param.detach().numpy().astype(np.float64)  # Convert to numpy array
                bytestr += arr.tobytes()
        elif self.MODEL_NAME == "AutoEncoder":
            for name, param in self.model[0].named_parameters():
                arr = param.detach().numpy().astype(np.float64)  # Convert to numpy array
                bytestr += arr.tobytes()
            for name, param in self.model[1].named_parameters():
                arr = param.detach().numpy().astype(np.float64)  # Convert to numpy array
                bytestr += arr.tobytes()
            for name, param in self.model[2].named_parameters():
                arr = param.detach().numpy().astype(np.float64)  # Convert to numpy array
                bytestr += arr.tobytes()
        return bytestr

    def from_bytes(self, bytestr):
        """
        Loads the byte representation of the autoencoder model's parameters.
        """
        if self.MODEL_NAME == "DBN":
            for layer in self.layers:
                if isinstance(layer, nn.Linear):
                    for param in layer.parameters():
                        arr = param.detach().numpy()
                        bytesize = arr.size * np.dtype(np.float64).itemsize
                        arr[:] = np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                        bytestr = bytestr[bytesize:]
        elif self.MODEL_NAME == "LSTMModel":
            for name, param in self.model.named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr[:] = np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
        elif self.MODEL_NAME == "AutoEncoder":
            for name, param in self.model[0].named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr[:] = np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
            for name, param in self.model[1].named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr[:] = np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
            for name, param in self.model[2].named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr[:] = np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
        assert len(bytestr) == 0

    def federate_from_bytes(self, bytestr, weight):
        """
        Given the byte representation of an autoencoder model and a weight, adds its parameters to this autoencoder model.
        """
        if self.MODEL_NAME == "DBN":
            for layer in self.layers:
                if isinstance(layer, nn.Linear):
                    for param in layer.parameters():
                        arr = param.detach().numpy()
                        bytesize = arr.size * np.dtype(np.float64).itemsize
                        arr += weight * np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                        bytestr = bytestr[bytesize:]
        elif self.MODEL_NAME == "LSTMModel":
            for name, param in self.model.named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr += weight * np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
        elif self.MODEL_NAME == "AutoEncoder":
            for name, param in self.model[0].named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr += weight * np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
            for name, param in self.model[1].named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr += weight * np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
            for name, param in self.model[2].named_parameters():
                arr = param.detach().numpy()
                bytesize = arr.size * np.dtype(np.float64).itemsize
                arr += weight * np.frombuffer(bytestr[:bytesize], dtype=np.float64).reshape(arr.shape)
                bytestr = bytestr[bytesize:]
        assert len(bytestr) == 0


