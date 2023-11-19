#!./env/bin/python
import random
import os
import csv
from timeit import default_timer as timer

from tqdm import tqdm # For progress bar of the loop
import matplotlib.pyplot as plt
import numpy as np

# Problem 1(a): Create a large random file 
def create_large_random_file(file_name):
    # Check whether the file already exists
    if os.path.exists(file_name):
        if input("File already exists. Overwrite?(y/n): ") == 'n':
            return None
    # Create the file
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Gender", "Age", "Country"])
        for _ in tqdm(range(10**8)):
            writer.writerow([random.randint(0, 1), #Gender
                             random.randint(0, 127), #Age
                             random.randint(0, 191)]) #Country

def read_csv(file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            yield row

def median_age(file_name, n):
    array_3d = np.zeros((2, 128, 192))
    index = 0
    result = {}
    start_read = timer()
    for row in read_csv(file_name):
        if index == n:
            break
        array_3d[int(row[0]), int(row[1]), int(row[2])] += 1
        index += 1
    end_read = timer()
    print("Time taken to read: {} seconds".format(end_read - start_read))

    for i in range(2):
        for k in range(192):
            tot = sum(array_3d[i, :, k])
            acc = 0
            for j in range(128):
                acc += array_3d[i, j, k]
                if acc >= tot/2:
                    result[(k, i)] = j
                    break
    return result

    
        

if __name__ == '__main__':
    file_name = 'large_file.csv'
    create_large_random_file(file_name)
    input_range = range((10**6), (10**8), 5*(10**6))
    elapsed_time = []
    for n in input_range:
        print("n = {}".format(n))
        start = timer()
        median_age(file_name, n)
        end = timer()
        elapsed_time.append(end - start)
        print("Time taken for the whole task: {} seconds".format(end - start))

    #plot

    plt.scatter(input_range, elapsed_time, marker='o', color='blue')
    plt.xlabel('input size')
    plt.ylabel('time taken')
    plt.savefig('problem_1.png')
    plt.show()