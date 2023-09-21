import matplotlib
import matplotlib.pyplot as plt
import pickle
import glob

path='./save/objects/*.pkl'
file_paths = glob.glob(path)
for file_name in file_paths:
    with open(file_name, 'rb') as f:
    # Load the objects using pickle.load
        train_loss, train_accuracy = pickle.load(f)
    matplotlib.use('Agg')
    plt.figure()
    plt.title('Training Loss vs Communication rounds')
    plt.plot(range(len(train_loss)), train_loss, color='r')
    plt.ylabel('Training loss')
    plt.xlabel('Communication Rounds')
    plt.savefig(f'{file_name[:-4]}loss.png')

    # Plot Average Accuracy vs Communication rounds
    plt.figure()
    plt.title('Average Accuracy vs Communication rounds')
    plt.plot(range(len(train_accuracy)), train_accuracy, color='k')
    plt.ylabel('Average Accuracy')
    plt.xlabel('Communication Rounds')
    plt.savefig(f'{file_name[:-4]}_acc.png')