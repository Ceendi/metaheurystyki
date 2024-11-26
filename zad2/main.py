from data import items
import random
import math


def create_initial_pop(population_size, max_weight):
    population = []
    items_count = len(items)

    for i in range(population_size):
        while True:
            individual_genes = [random.choice([0, 1]) for _ in range(items_count)]
            weight_sum = sum([items[i]['weight'] * gene for i, gene in enumerate(individual_genes)])
            if weight_sum <= max_weight:
                break

        population.append(individual_genes)

    return population


def fitness_function(individual, max_weight):
    i_weight = 0
    i_value = 0
    for i, gene in enumerate(individual):
        i_weight += gene * items[i]['weight']
        i_value += gene * items[i]['value']
    if i_weight > max_weight:
        i_value = 0
    return i_value ** 2 / i_weight if i_weight != 0 else 0


def summ(individual, max_weight):
    i_weight = 0
    i_value = 0
    for i, gene in enumerate(individual):
        i_weight += gene * items[i]['weight']
        i_value += gene * items[i]['value']
    if i_weight > max_weight:
        i_value = 0
    return i_value, i_weight


def roulette_selection(population, fitnesses, crossover_rate):
    probabilities = [value / sum(fitnesses) for value in fitnesses]
    parents = random.choices(population, weights=probabilities, k=int(len(population) * crossover_rate))
    return parents


def elite_selection(population, fitnesses, crossover_rate):
    sorted_fitnesses, sorted_population = zip(*sorted(zip(fitnesses, population), reverse=True))
    return sorted_population[:int(len(population) * crossover_rate)]


def single_point_crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(1, len(parent1)), 2))
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2


def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = individual[i] ^ 1

    return individual


def genetic_algorithm(population_size, generations, mutation_rate, crossover_rate, max_weight):
    population = create_initial_pop(population_size, max_weight)
    best_fit = 0
    for generation in range(generations):
        fitnesses = [fitness_function(ind, max_weight) for ind in population]

        new_best_fitness = max(fitnesses)
        new_best_individual = population[fitnesses.index(new_best_fitness)]
        if new_best_fitness > best_fit:
            best_fit = new_best_fitness
            best_individual = new_best_individual

        parents = elite_selection(population, fitnesses, crossover_rate)

        next_population = []
        while len(next_population) < population_size:
            index1, index2 = random.sample(range(len(parents)), 2)
            parent1, parent2 = parents[index1], parents[index2]

            child1, child2 = two_point_crossover(parent1, parent2)

            next_population.append(mutation(child1, mutation_rate))
            next_population.append(mutation(child2, mutation_rate))

        population = next_population

        print(new_best_individual, summ(new_best_individual, max_weight))

    print(f'BEST INDIVIDIAL:{best_individual}, {summ(best_individual, max_weight)}')


genetic_algorithm(500, 500, 0.01, 0.8, 6_404_180)
# 13 692 887 dla 6 397 822
