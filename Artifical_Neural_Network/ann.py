from ann_util import sigmoid, sigmoid_d
import numpy as np
import csv

class Layer:    
    def __init__(self, num_neurons, num_inputs, act, act_d):
        self.w = np.random.uniform(-0.1, 0.1, (num_neurons, num_inputs))
        self.b = np.zeros(num_neurons)  # Bias
        self.z = np.zeros(num_neurons)  # Weighted input
        self.o = np.zeros(num_neurons)  # Activations/outputs  # eller "a"?
        self.act = act
        self.act_d = act_d
        self.__shape = (num_neurons, num_inputs)
        
    def __len__(self):
        return self.__shape[0]
    
    @property
    def prev(self):
        return self.__prev_layer
    
    @property
    def next(self):
        return self.__next_layer
    
    def set_prev(self, prev_layer):
        self.__prev_layer = prev_layer
        
    def set_next(self, next_layer):
        self.__next_layer = next_layer


class ANN:
    def __init__(self, layer_sizes, learning_rate=0.01, act_h=(sigmoid,sigmoid_d), act_o=(sigmoid,sigmoid_d)):
        if len(layer_sizes) < 3:
            raise ValueError("There must be a minimum of 3 layers")
        self.layers = []
        self.learning_rate = learning_rate
        
        # Initialize layers
        for size, prev_size in zip(layer_sizes[1:], layer_sizes):
            self.layers.append(Layer(size, prev_size, *act_h))
        self.layers[-1].act_func, self.layers[-1].act_func_d = act_o[0], act_o[1] # output
        for i, l in enumerate(self.layers):
            l.set_prev(None if i == 0 else self.layers[i - 1])
            l.set_next(None if i == len(self.layers) - 1 else self.layers[i + 1])
            
    def feed_forward(self, x):
        for layer in self.layers:
            layer.z = np.dot(layer.w, x) + layer.b
            layer.o = layer.act(layer.z)
            x = layer.o
        return x
    
    def backprop(self, inputs, target, lr):
        # Calculate errors for output layer
        self.layers[-1].e = (self.layers[-1].o - target) * self.layers[-1].act_d(self.layers[-1].z)
        
        # Calculate errors for hidden layers
        for layer in self.layers[-2::-1]:
            layer.e = np.dot(layer.next.e, layer.next.w) * layer.act_d(layer.z)
            
        self.layers[0].set_prev(type('Layer', (object,), {'o' : inputs}))
        for layer in self.layers[::-1]:
            # Calculate Cost'(w)
            error_d = layer.prev.o * np.vstack(layer.e)

            # Update weights and biases
            layer.w -= lr * error_d
            layer.b -= layer.e

    def train(self, training_set, validation_set, num_epochs=2):
        
        # Temp - Check validation set accuracy during training and write results to file
        # f = open('val_acc.csv', mode='w')
        # csv_writer = csv.writer(f, delimiter=',', lineterminator='\r')
        # csv_writer.writerow(["num_train","training_set_index","validation_accuracy"])
        
        for epoch in range(0, num_epochs):
            lr = self.learning_rate / (epoch + 1)

            for i, data in enumerate(training_set, start=1):
                self.feed_forward(data.values)
                self.backprop(data.values, data.label, lr)
                
                # Temp - validation check
                # if i in {1, len(training_set)} or not i % 100:
                #     # Calculate accuracy of validation set
                #     _, res = self.eval_data_set(validation_set)
                #     acc = np.divide(*res)
                #     csv_writer.writerow([str(i + len(training_set) * epoch), str(i), str(acc)])
                    
                if not i % 100 or i == len(training_set):                    
                    print(f"\rProgress: {i}/{len(training_set)}, epoch: {epoch + 1}/{num_epochs}, lr: {lr:.05f}\t", end="")
                   
        # Temp - validation check
        # f.close()
    
    def eval_data_set(self, data_set, print_progress=False):
        results = []
        for i, data in enumerate(data_set, start=1):
            results.append(self.eval(data))
            if print_progress and (not i % 100 or i == len(data_set)):
                print(f"\rProgress: {i}/{len(data_set)}", end="")

        lbl, pred = np.array(results).T # TODO: Fix unpack error (it currently works though)
        res_cls = [(np.where((lbl==i) & (pred==i))[0].size, (lbl==i).sum()) for i in range(0, 10)]
        res_tot = (sum(x for x,_ in res_cls), len(results))
        return res_cls, res_tot
        #return sum(x == y for x,y in results), len(results) # correct predictions, number of predictions
    
    def eval(self, data):
        prediction = self.feed_forward(data.values)
        result = tuple(np.argmax([data.label, prediction], axis=1))
        return result
