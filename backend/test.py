from ModelConfig import AutoencoderWithClassifier
from config import config 
from utils import *
from dataPreProcess import load_dataset
from Blockchain import Blockchain, ModelTransaction,Block
from model import *
blockchain = Blockchain()

def localUpdate():
    per = 20
    dataset  = load_dataset(config.Train,config.Test,config.BATCH_SIZE)

    size,mean,std = localStatistics(dataset.train)
    last_block = blockchain.chain[-1]
    if last_block.transactions:
        last_transaction = last_block.transactions[-1]
        block_data = {
            'model_bytes':last_transaction.model_bytes,
            'mean': last_transaction.mean.tolist(),
            'std_dev': last_transaction.std_dev.tolist(),
            'size': last_transaction.size
        }
    mean = Combined_Mean(mean, size ,block_data['mean'],block_data['size']) 
    std = Combined_Std(std, size, block_data['std_dev'], block_data['size'])
    autoencoder = AutoencoderWithClassifier(config.INPUT_SIZE, config.NUM_CLASSES)
    train_model(autoencoder, dataset.train, config.NUM_EPOCHS, config.LEARNING_RATE, mean, std)
    evaluate_model(autoencoder, dataset.test,block_data)
    weight = size / (size + block_data['size'])
    autoencoder.federate_from_bytes(block_data['model_bytes'],weight)
    model_tx = ModelTransaction(autoencoder.to_bytes(), mean, std )
    blockchain.add_transaction(model_tx)
    blockchain.mine_block()
    last_block = blockchain.chain[-1]
    if last_block.transactions:
        last_transaction = last_block.transactions[-1]
        block_data = {
            'model_bytes':last_transaction.model_bytes.hex(),
            'mean': last_transaction.mean.tolist(),
            'std_dev': last_transaction.std_dev.tolist(),
            'size': last_transaction.size
        }
    
    
if __name__ == "__main__":
    global_model = AutoencoderWithClassifier(config.INPUT_SIZE, config.NUM_CLASSES)
    model_tx = ModelTransaction(global_model.to_bytes(), np.zeros((1, 118), dtype=np.float64), np.ones((1, 118), dtype=np.float64) )
    blockchain.add_transaction(model_tx)
    blockchain.mine_block()
    localUpdate()