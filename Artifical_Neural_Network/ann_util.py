import numpy as np
np.seterr(over='ignore', divide='ignore') # Ignore overflow

# Activation functions
def sigmoid(x):     return 1.0 / (1.0 + np.exp(-x))         # (0, 1) 
def sigmoid_d(x):   return sigmoid(x) * (1.0 - sigmoid(x))
def relu(x):        return np.maximum(0.0, x)               # [0, inf)
def relu_d(x):      return (x > 0).astype(float)
def tanh(x):        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x)) # (-1, 1)
def tanh_d(x):      return 1 - (tanh(x) ** 2)
def softmax(x):     return np.exp(x) / sum(np.exp(x))       # (0, 1) 

# Cost function
def MSE(y, a):      return (np.sum((a - y) ** 2)).mean()    # y = target, a = prediction
def MSE_d(y, a):    return (2 / len(y)) * np.sum(a - y)