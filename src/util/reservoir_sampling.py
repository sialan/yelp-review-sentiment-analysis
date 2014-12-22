import random


def generate_sample(n, population):
    sample = [];
     
    for i, item in enumerate(population):
        if i < n:
            sample.append(item)
        elif i >= n and random.random() < n/float(i + 1):
            replace = random.randint(0, len(sample) - 1)
            sample[replace] = item
    return sample

if __name__ == '__main__':
    # Return random sample of 1000 elements from 0 - 1 000 000
    sample_size = 1000
    population_ids = range(0, 1000000)
    sample_ids = generate_sample(sample_size, population_ids)
    print(sample_ids)
