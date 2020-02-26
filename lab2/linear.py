import random
import vector
import datasets
import matplotlib.pyplot as plt

def normalize(observations):
    return observations

def stoch_descent(X, y, alpha, w):
    return w

def batch_descent(X, y, alpha, w):
    return w

if __name__ == '__main__':
    normalized = True
    debug = False
    X, y = datasets.read_tsv('resources/salammbo_a_en.tsv')
    print(X, y)