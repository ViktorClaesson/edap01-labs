import random
import vector
import datasets
import numpy as np
import matplotlib.pyplot as plt

def normalize(obs):
    print(obs)
    maxima = np.amax(obs, axis=0)
    print(maxima)
    D = np.diag(maxima)
    print(D)
    D_inv = np.linalg.inv(D)
    print(D_inv)
    obs = obs @ D_inv
    print(obs)
    return (obs, maxima)


def stoch_descent(X, y, alpha, w):
    return w


def batch_descent(X, y, alpha, w):
    alpha /= len(X)
    



    return w


if __name__ == '__main__':
    X_en, y_en = datasets.read_tsv('resources/salammbo_a_en.tsv')
    
    normalize(X_en)
    #w = batch_descent(X_en, y_en, 0.001, w)