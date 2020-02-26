from svm_reader import parse_data
from gradient_descent import stoch_descent
import numpy as np
import random
import matplotlib.pyplot as plt

def perceptron(X, label, alpha, w, idx):
    for epoch in range(500):
        alpha = 1000 / (1000 + epoch)
        missclassified = 0
        random.shuffle(idx)
        for i in idx:
            x = X[i]
            label_i = label[i]
            hw = 1.0 if (np.dot(w.T, x)[0] >= 0.0) else 0.0
            if label_i == 1.0 and hw == 0.0:
                missclassified += 1
                for i in range(len(x)):
                    w[i][0] = w[i][0] + x[i] * alpha
            if label_i == 0.0 and hw == 1.0:
                missclassified += 1
                for i in range(len(x)):
                    w[i][0] = w[i][0] + x[i] * -alpha
        if missclassified == 0:
            break
    print('Epoch: {}'.format(epoch))
    return w

def perceptron_loocv(X, label, alpha, w):
    idx = list(range(len(X)))
    correct = 0
    
    for i in range(len(X)):
        random.shuffle(idx)
        loo_idx = idx.pop(0)
        w = np.zeros(X.shape[1]).reshape((-1,1))
        w = perceptron(X, label, alpha, w, idx)
        hw = 1.0 if (np.dot(w.T, X[loo_idx])[0] >= 0.0) else 0.0
        if hw == label[loo_idx]:
            correct += 1
        idx.append(loo_idx)
    print(correct)
    return w

def plot_points(lang, color):
    print(lang)
    x = [xs[0] for xs in lang]
    y = [xs[1] for xs in lang]
    plt.plot(x, y, color)

def plot(en, fr, W):
    print("Weights: {0}".format(W))
    k = W[1][0] / -W[2][0]
    m = W[0][0] / -W[2][0]
    print("y = {0}x + {1}".format(k, m))
    plot_points(en, 'r*')
    plot_points(fr, 'b*')
    x = range(85000)
    plt.plot(x, (x*k + m), 'c-')
    plt.xlim(10000, 85000)
    plt.show()

if __name__ == "__main__":
    en, fr = parse_data('data/data.libsvm')
    
    X = [[1.0, en[i][0], en[i][1]] for i in range(len(en))] + [[1.0, fr[i][0], fr[i][1]] for i in range(len(fr))]
    X = np.array(X)
    w = np.zeros(X.shape[1]).reshape((-1,1))
    # print(X)
    label = [0.0 for _ in range(len(en))] + [1.0 for _ in range(len(fr))]
    alpha = 1.0

    w = perceptron(X, label, alpha, w, list(range(len(X))))
    plot(en, fr, w)

    w = np.zeros(X.shape[1]).reshape((-1,1))
    
    w = perceptron_loocv(X, label, alpha, w)
    plot(en, fr, w)