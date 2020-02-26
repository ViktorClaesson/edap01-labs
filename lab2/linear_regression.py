import random
import datasets
import numpy as np
import sys
import matplotlib.pyplot as plt

def normalize(obs):
    maxima = np.amax(obs, axis=0)
    D = np.diag(maxima)
    D_inv = np.linalg.inv(D)
    obs = obs @ D_inv
    return (obs, maxima)


def stoch_descent(X, y, alpha, w):
    index_list = list(range(len(X)))
    for epoch in range(500):
        random.shuffle(index_list)
        w_old = w
        for i in index_list:
            w = w + alpha * np.array([X[i]]).T * (y[i] - X[i] @ w)
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.005:
            print(f'Epoch {epoch}')
            break
    return w


def batch_descent(X, y, alpha, w):
    alpha /= len(X)

    for epoch in range(500):
        w_old = w
        w = w + alpha * X.T @ (y - X @ w)
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.005:
            print(f'Epoch: {epoch}')
            break

    return w


def plot(X, y, x0, x1):
    plt.plot(X, y, 'r*')
    plt.plot(x0, x1, 'b-')
    plt.show()
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Require <en> or <fr> as an argument')
        exit()
    
    if sys.argv[1] == 'en':
        X, y = datasets.read_tsv('resources/salammbo_a_en.tsv')
    elif sys.argv[1] == 'fr':
        X, y = datasets.read_tsv('resources/salammbo_a_fr.tsv')

    X = np.array(X)
    y = np.array([y]).T

    print(' --- STOCH --- ')

    X_norm, X_maxima = normalize(X)
    y_norm, y_maxima = normalize(y)

    w = np.zeros(X.shape[1]).reshape((-1, 1))

    w = stoch_descent(X_norm, y_norm, 0.05, w)
    print(w)

    X_plot = [xs[1] for xs in X]
    y_plot = y
    x = np.linspace(0, 1)

    plot(X_plot, y_plot, x * X_maxima[1], (w[1] * x + w[0]) * y_maxima)

    print(' --- BATCH --- ')

    w = np.zeros(X.shape[1]).reshape((-1, 1))

    w = batch_descent(X_norm, y_norm, 1, w)
    print(w)

    X_plot = [xs[1] for xs in X]
    y_plot = y
    x = np.linspace(0, 1)

    plot(X_plot, y_plot, x * X_maxima[1], (w[1] * x + w[0]) * y_maxima)


