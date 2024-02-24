import random
from matplotlib import pyplot as plt
import numpy as np

def generate_random_number_exponential_distribution(lmbd, size = 1):
    random_numbers = np.random.exponential(scale=1/lmbd, size=size)
    random_numbers_int = random_numbers.round().astype(int)
    if size == 1:
        return random_numbers_int[0]
    return random_numbers_int.tolist()

def generate_random_number_normal_distribution(mean, size = 1):
    random_numbers = np.random.normal(loc=mean, scale=1, size=size)
    random_numbers_int = random_numbers.round().astype(int)
    if size == 1:
        return random_numbers_int[0]
    return random_numbers_int.tolist()

def plot_histogram(*data):
    for data in data:
        plt.hist(data, bins=40, alpha=0.5)
    plt.xlabel('Value')
    plt.ylabel('Number of elements')
    plt.show()



random_numbers1 = generate_random_number_exponential_distribution(0.3, size=10)

random_numbers2 = generate_random_number_normal_distribution(0, size=10)

plot_histogram(random_numbers1, random_numbers2)

