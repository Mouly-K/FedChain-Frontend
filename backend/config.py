import os
class config:
    DEBUG = False
    NUM_EPOCHS = int(os.environ.get('NUM_EPOCHS', 10))
    LEARNING_RATE = float(os.environ.get('LEARNING_RATE', 0.001))
    BATCH_SIZE = int(os.environ.get('BATCH_SIZE', 64))
    TEST_SIZE = float(os.environ.get('TEST_SIZE', 0.2))
    THRESHOLD = float(os.environ.get('THRESHOLD', 0.15))
    INPUT_SIZE = 118
    NUM_CLASSES = 2
    Train= 'dataset/train/'
    Test= 'dataset/test/test_data.csv'
    DatasetPath='dataset/nid.csv'
    initialTrain = 'dataset/train/data1.csv'
    ModeName = 'LSTMModel'
    NUM_DATA = 5
    certificate = './ssl/certificate.pem'
    private_key = './ssl/private_key.pem'
    relayChain = 'https://localhost:5000'
