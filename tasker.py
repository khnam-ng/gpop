import numpy as np

class Tasker():
    def __init__(self):
        pass

    def task_1(self, p, N):
        print('Task 1: Genetic drift')
        population = np.random.choice(['A', 'B'], size=N, p=[p, 1 - p])
        generations = 2*N #each new generation is obtained from the previous generation 2N times
        allele_freqs = []

        for gen in range(generations): 
            allele_freq_A = np.sum(population == 'A') / N #Pt depends on Pt-1
            allele_freqs.append(allele_freq_A)
            
            #choosing an allele at random
            #Each individual in generation t+1 is a copy of a randomly selected individual in generation t.
            population = np.random.choice(population, size=N, replace=True)
            
            #fixation
            if allele_freq_A == 1 or allele_freq_A == 0:
                break
        return allele_freqs
                              
    def task_2_identicalByDescent(self, N):
        print('Task 2: Coalescent model + identical by descent')
        population = np.arange(N)
        generations = 0
        freq = []
        freq.append(1/N) #population has N alleles then first frequency of each allele = 1/N

        while len(set(population)) > 1:  #unique number in population, stop when population has only one number left.
            generations += 1
            #Each individual in generation t+1 is a copy of a randomly selected individual in generation t.
            population = np.random.choice(population, size=N, replace=True)
            #If True, also return the number of times each unique item appears in ar.
            unique, counts = np.unique(population, return_counts=True)
            freq.append(np.max(counts) / N)
        
        return generations, freq

    def task_2_firstCoalescentEvent(self, n, N):
        print('Task 2: First coalescent event + sample size')
        generations = 0
        while 1:
            generations += 1
            coalescent_proba = n*(n-1)/(2*N)
            if np.random.rand() < coalescent_proba:
                break
        return generations
    def task_2_coalescentModel(self, n, N):
        print('Task 2: Coalescent model + sample size')
        generations = 0
        while n > 1:
            generations += 1
            coalescent_proba = n*(n-1)/(2*N)
            if np.random.rand() < coalescent_proba:
                n -= 1
        return generations
    def task_3(self, N, mutation_rate, generations):
        print('Task 3: Mutations in the infinite-allele model')
        population = np.zeros(N, dtype=int)  #Start from an initially homogeneous population of N identical alleles
        fixation_index = []

        for gen in range(generations):
            unique, counts = np.unique(population, return_counts=True)
            freq = counts / N
            fixation_index.append((1-mutation_rate**2)*((1/N)+(1-(1/N))*np.sum(freq ** 2)))

            offspring = np.random.choice(population, size=N)
            
            mutations = np.random.rand(N) < mutation_rate #return True if rand < mutation_rate
            #change values in offspring by random integers from 0 to np.sum(mutations) [like from 0 to 10], using index of True variable in mutations array to refill values in offsping array.
            offspring[mutations] = np.random.randint(np.sum(mutations), size=np.sum(mutations)) 
            population = offspring
         
        return fixation_index

    def task_4(self, N, p, s, generations):
        # the selection can be fitness dependent, 
        # or mutations between parent and offspring may appear with some mutation rate.
        print('Task 4: Selection')
        population = np.random.choice(['A', 'B'], size=N, p=[p, 1 - p])
        freq_B = []
        for gen in range(generations):
            fitness = {'A': 1, 'B': 1 + s}
            #The fitness is realized by selecting a parent allele with a probability proportional to fitness from the parent population
            selection_proba = np.array([fitness[allele] for allele in population])
            selection_proba /= np.sum(selection_proba)
            
            population = np.random.choice(population, size=N, p=selection_proba)
            
            freq_B.append(np.sum(population == 'B') / N)
        return freq_B
    
    def task_5(self, N, generations, pA = 0.79, pB = 0.2, pC = 0.01):
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

