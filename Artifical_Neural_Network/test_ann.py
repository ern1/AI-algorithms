from ann import ANN
import ann_util as utl
import numpy as np
import math
import csv
import dill
from traceback import print_exc
#import pdb

class Img:
    def __init__(self, label, values):
        self.label = label
        self.values = values

class DataSets:
    def __init__(self, file_path, label_size, value_size):
        self.label_size = label_size    # number of classes
        self.value_size = value_size
        self.load_datasets(file_path)

    def read_file(self, file_path):
        data_set = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip first line
            for row in csv_reader:
                row = list(map(int, row))
                target_arr = np.zeros(10)
                target_arr[row[0]] = 1.0
                data_set.append(Img(target_arr, np.array(row[1:])))

        # Split data set: 70% training, 10% validation, 20% test
        size = len(data_set)
        x, y = math.floor(size * 0.7), math.floor(size * 0.8)
        self.training = np.array(data_set[:x])
        self.validation = np.array(data_set[x:y])
        self.test = np.array(data_set[y:])

    def load_datasets(self, file_path):
        try:
            with open('data.pkl', 'rb') as fp:
                self.training, self.validation, self.test = dill.load(fp)
        except FileNotFoundError:
            print(f'Could not find data.pkl - Reading from {file_path}')
            self.read_file(file_path)
            with open('data.pkl', 'wb') as fp:
                dill.dump(
                    (self.training, self.validation, self.test),
                    fp,
                    protocol=dill.HIGHEST_PROTOCOL,
                )
        except Exception:
            print_exc()


def main():
    print("Loading data sets...")
    data_sets = DataSets("mnist_train.csv", 10, 784)
    
    print("Initializing network...")
    layer_sizes = [
        data_sets.value_size,   # input
        300,                    # hidden (1)
        100,                    # hidden (2)
        data_sets.label_size,   # output
    ]
    network = ANN(
        layer_sizes,
        learning_rate = 0.01,
        # Default activation function is sigmoid/sigmoid_d for all layers
        #act_h = (utl.relu, utl.relu_d),
        #act_h = (utl.tanh, utl.tanh_d),
        act_o = (utl.softmax, lambda: 1)
    )

    print(f"Training network...")
    network.train(data_sets.training, data_sets.validation, num_epochs=2)
   
    print(f"\n\rEvaluating network...")
    result_class, result_total = network.eval_data_set(data_sets.test, print_progress=True)

    print("\n\n\rResult, per class:\n", "\n ".join(f"{i}: {pred} out of {size} ({round(pred/size, 4)})" for i, (pred,size) in enumerate(result_class)))
    print(f"\nResult, total: {result_total[0]} out of {result_total[1]} ({round(np.divide(*result_total), 4)})")
    
if __name__ == '__main__':
    main()
