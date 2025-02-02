import numpy as np
from urllib.request import urlopen

def read_libsvm(file_path):
    """
    Read a libsvm file. The format is not sparse
    :param file_path:
    :return: X, y as lists
    """
    data = open(file_path).read().strip().split('\n')
    observations = [data[i].split() for i in range(len(data))]

    y = [float(obs[0]) for obs in observations]
    # We add the intercept
    X = [['0:1'] + obs[1:] for obs in observations]
    X = [list(map(lambda x: float(x.split(':')[1]), obs)) for obs in X]
    return X, y


def read_tsv(file_path):
    """
    Read a tsv file. The response is the last column
    :param file_path:
    :return: X, y as lists
    """
    observations = open(file_path).read().strip().split('\n')
    observations = [[1] + list(map(float, obs.split())) for obs in observations]
    X = [obs[:-1] for obs in observations]
    y = [obs[-1] for obs in observations]
    return X, y

if __name__ == '__main__':
    X, y = read_tsv('resources/salammbo_a_en.tsv')
    print('X:', X)
    print('y:', y)
    X, y = read_libsvm('resources/salammbo_a.libsvm')
    print('X:', X)
    print('y:', y)
