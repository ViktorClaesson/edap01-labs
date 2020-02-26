from gradient_descent import stoch_descent
import numpy as np
import random
import datasets
import matplotlib.pyplot as plt

def perceptron(X, y, alpha, w, index_list):
    for epoch in range(500):
        alpha = 1000 / (1000 + epoch)
        random.shuffle(index_list)
        missclassified = 0
        for i in index_list:
            x = X[i]
            y_i = y[i]
            h_w = 1.0 if (np.dot(w.T, x)[0] >= 0.0) else 0.0
            if y_i == 0.0 and h_w == 1.0:
                missclassified += 1
                for i in range(len(x)):
                    w[i][0] = w[i][0] + x[i] * -alpha
            if y_i == 1.0 and h_w == 0.0:
                missclassified += 1
                for i in range(len(x)):
                    w[i][0] = w[i][0] + x[i] * alpha
        if missclassified == 0:
            break
    print('Epoch: {}'.format(epoch))
    return w

def perceptron2(X, y, alpha, w):
    index_list = list(range(len(X)))
    correct = 0
    
    for i in range(len(X)):
        random.shuffle(index_list)
        loo_index = index_list.pop(0)
        w = np.zeros(X.shape[1]).reshape((-1,1))
        w = perceptron(X, y, alpha, w, index_list)
        h_w = 1.0 if (np.dot(w.T, X[loo_index])[0] >= 0.0) else 0.0
        if h_w == y[loo_index]:
            correct += 1
        index_list.append(loo_index)
    print(correct)
    return w

def plot(X, y, w):
    print("Weights: {0}".format(w))
    k = w[1][0] / -w[2][0]
    m = w[0][0] / -w[2][0]
    print("y = {0}x + {1}".format(k, m))
    plt.plot([X[i][1] for i in range(len(X)) if y[i] == 0], [X[i][2] for i in range(len(X)) if y[i] == 0], 'r*')
    plt.plot([X[i][1] for i in range(len(X)) if y[i] == 1], [X[i][2] for i in range(len(X)) if y[i] == 1], 'b*')
    x = range(85000)
    plt.plot(x, (x*k + m), 'c-')
    plt.xlim(10000, 85000)
    plt.show()

if __name__ == "__main__":
    X, y = datasets.read_libsvm('resources/salammbo_a.libsvm')
    X = np.array(X)
    w = np.zeros(X.shape[1]).reshape((-1,1))
    
    print(X)

    alpha = 1.0

    w = perceptron(X, y, alpha, w, list(range(len(X))))
    plot(X, y, w)

    w = np.zeros(X.shape[1]).reshape((-1,1))
    
    w = perceptron2(X, y, alpha, w)
    plot(X, y, w)