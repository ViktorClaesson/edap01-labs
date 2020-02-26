import numpy as np
import random
import datasets
import matplotlib.pyplot as plt

def threshold(w, x):
    return 1 / (1 + np.exp(-w @ x))

def logistic_regression(X, y, w, idx, alpha=1.0):
    # idx = list(range(len(X)))
    for epoch in range(500):
        random.shuffle(idx)
        w_old = w
        for i in idx:
            w = w + alpha * X[i] * (y[i] - threshold(w, X[i]))
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.005:
            print('Epoch: {}'.format(epoch))
            break
    return w

def loocv_logreg(X, y, w, alpha=1.0):
    idx = list(range(len(X)))
    correct = 0

    for i in range(len(X)):
        random.shuffle(idx)
        loo_idx = idx.pop(0)
        w = np.zeros(len(X[0]))
        w = logistic_regression(X, y, w, idx)
        hw = 1.0 if (threshold(w, X[loo_idx]) >= 0.5) else 0.0
        if hw == y[loo_idx]:
            correct += 1
        idx.append(loo_idx)
    print('Correct: {}'.format(correct))
    return w

def norm_val(vals, W):
    print(vals[0])
    return np.linalg.norm([W @ xs for xs in vals])

def plot_log_points(lang, W, color, norm):
    x = [np.dot(W, xs)/norm for xs in lang]
    y = [1 / (1 + np.exp(-e*norm)) for e in x]
    plt.plot(x, y, color)

def plot_log(en, fr, W):
    k = W[1] / -W[2]
    m = W[0] / -W[2]
    print("Weights: {0}".format(W))
    print("y = {0}x + {1}".format(k, m))
    norm = norm_val(np.concatenate((en, fr)), W)
    print("Norm {0}".format(norm))
    plot_log_points(en, W, 'r*', norm)
    plot_log_points(fr, W, 'b*', norm)
    plt.show()

if __name__ == "__main__":
    X, y = datasets.read_libsvm('resources/salammbo_a.libsvm')
    X = np.array(X)
    y = np.array(y)
    w = np.zeros(len(X[0]))

    alpha = 1.0

    w = logistic_regression(X, y, w, list(range(len(X))))
    print(w)
    plot_log(X[:15], X[15:], w)

    print('-' * 20)

    w = np.zeros(len(X[0]))
    w = loocv_logreg(X, y, w)
    print(w)
    plot_log(X[:15], X[15:], w)