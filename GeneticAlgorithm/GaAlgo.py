import numpy as np
import string
import random
from pprint import pprint
import matplotlib.pyplot as plt


class Population:
    def __init__(self, pop_size, target, mutate_proba=0.01):
        self.pop_size = pop_size
        self.target = target
        self.mutate_proba = mutate_proba
        self.dna_size = len(target)
        self.entities = [Entitie(dna_size=self.dna_size) for _ in range(pop_size)]

    def __repr__(self):
        return str(self.entities)

    # fitness function
    def proba_of_importance(self):
        fitness_scores = np.array([entitie.fitness_score(self.target) for entitie in self.entities])
        #normalized_fitness = fitness_scores / np.sum(fitness_scores)
        return fitness_scores

    # Selection: the group of population that have the permission to reproduce the next generation
    def pick_reproduction_group(self):
        # generate pairs of parents(size=2)=> array([first_parrent, second_parent])
        # who had the permission for reproduction
        fitness_scores = self.proba_of_importance()
        selected = {k: v for k, v in zip(self.entities, fitness_scores)}
        selected = sorted(selected.items(), key=lambda x: x[1], reverse=True)
        selected = selected[: int(len(selected) * 0.2)]
        group_permission = [x[0] for x in selected]
        for _ in range(self.pop_size):
            yield np.random.choice(group_permission, size=2)
    
    # CrossOver
    def crossover_random_single_point(self, first_parrent, second_parent):
        assert len(first_parrent) == len(second_parent)
        single_point = random.randint(0, len(first_parrent) - 1)
        first_part = first_parrent.dna[: single_point]
        second_part = second_parent.dna[single_point :]
        first_part.extend(second_part)
        new_child = first_part
        return new_child

    @staticmethod
    def choose_random_alphabet():
        alphabet = string.ascii_letters + ' ' + '0123456789' + string.punctuation
        return random.choice(list(alphabet))

    # Mutation: change some parent DNA for having new characteristics
    def mutate_new_child(self, new_child):
        for index in range(len(new_child)):
            if np.random.random_sample() <= self.mutate_proba:
                new_child[index] = Population.choose_random_alphabet()
        return new_child

    def create_new_generation(self):
        new_population = []
        for pairs_parent in self.pick_reproduction_group():
            new_child = self.crossover_random_single_point(pairs_parent[0], pairs_parent[1])
            new_child = self.mutate_new_child(new_child)
            new_entitie = Entitie(dna=new_child)
            new_population.append(new_entitie)
        self.entities = new_population
        

class Entitie:
    def __init__(self, dna_size=None, dna=None):
        self.dna_size = dna_size if dna_size else len(dna)
        self.dna = dna if dna else self.random_choice_dna()
       
    def __repr__(self):
        return ''.join(self.dna)

    def __iter__(self):
        return iter(self.dna)

    def __len__(self):
        return len(self.dna)
    
    def random_choice_dna(self):
        alphabet = string.ascii_letters + ' ' + '0123456789' + string.punctuation
        return random.sample(alphabet, self.dna_size)

    def fitness_score(self, other):
        similarity = 0
        for x, y in zip(self.dna, other):
            if x == y:
                similarity += 1
        return similarity / self.dna_size
