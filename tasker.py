import numpy as np
# import matplotlib.pyplot as plt

class Tasker():
    def __init__(self):
        pass
    
    def task_1(self, p, N):
        print('Task 1: Genetic drift')
        q = 1 - p

    def task_2(self, p, N = 100):
        print('Task 2: Coalescent model')

    def task_3(self, p, N, mutation_rate):
        print('Task 3: Mutations in the infinite-allele model')

    def task_4(self):
        # the selection can be fitness dependent, 
        # or mutations between parent and offspring may appear with some mutation rate.
        print('Task 4: Selection')
    
    def task_5(self, pA = 0.79, pB = 0.2, pC = 0.01, N = 100):
        print('Task 5: Clonal inference')
    
    def task_6(self):
        # Divide the population of Task 1 now in 10 equally large sub-populations. Simulate the
        # system with a complete separation of the sub-populations: parents are selected only in the
        # same subpopulation, and no mutation, selection or migration exists
        print('Task 6: Population structure')

    def task_7(self):
        # a migration of a fraction m = 0.1 of each   
        # population towards and from randomly chosen subpopulations (i.e. the subpopulations
        # exchange individuals, but remain of the same size)  
        print('Task 7: Migration')

