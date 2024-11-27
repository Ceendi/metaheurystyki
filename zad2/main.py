from data import items
import random
import math
from matplotlib import pyplot as plt


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


def get_value_weight(individual, max_weight):
    i_weight = 0
    i_value = 0
    for i, gene in enumerate(individual):
        i_weight += gene * items[i]['weight']
        i_value += gene * items[i]['value']
    if i_weight > max_weight:
        i_value = 0
    return i_value, i_weight


def roulette_selection(population, fitnesses, crossover_rate):
    assert 0 < crossover_rate < 1
    probabilities = [value / sum(fitnesses) for value in fitnesses]
    parents = random.choices(population, weights=probabilities, k=int(len(population) * crossover_rate))
    return parents


def tournament_selection(population, fitnesses, group_count):
    assert group_count >= 2 or isinstance(group_count, int) or group_count > len(population)
    group_size = len(population) // group_count

    population_copy = list(zip(population, fitnesses))

    parents = []
    for _ in range(group_count):
        contestants = random.sample(population_copy, group_size)
        winner = max(contestants, key=lambda x: x[1])
        parents.append(winner[0])

        for contestant in contestants:
            population_copy.remove(contestant)

    return parents


def elite_selection(population, fitnesses, crossover_rate):
    assert 0 < crossover_rate < 1
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


def genetic_algorithm(population_size, generations, mutation_rate, selection, param, crossover, max_weight):
    population = create_initial_pop(population_size, max_weight)
    best_fit = -math.inf
    best_individuals = []
    best_gen_individuals = []
    best_individual = None

    for generation in range(generations):
        fitnesses = [fitness_function(ind, max_weight) for ind in population]

        new_best_fitness = max(fitnesses)
        new_best_individual = population[fitnesses.index(new_best_fitness)]
        if new_best_fitness > best_fit:
            best_fit = new_best_fitness
            best_individual = new_best_individual
        best_individuals.append(new_best_individual)
        best_gen_individuals.append(best_individual)

        parents = selection(population, fitnesses, param)

        next_population = []
        while len(next_population) < population_size:
            index1, index2 = random.sample(range(len(parents)), 2)
            parent1, parent2 = parents[index1], parents[index2]

            child1, child2 = crossover(parent1, parent2)

            next_population.append(mutation(child1, mutation_rate))
            next_population.append(mutation(child2, mutation_rate))

        population = next_population

    return best_individual, best_individuals, best_gen_individuals


def start(population_size, generations, mutation_rate, selection, param, crossover, max_weight):
    fig, axs = plt.subplots(5, 2, figsize=(10, 16))

    for i in range(5):
        best_individual, best_individuals, best_gen_individuals = (
            genetic_algorithm(population_size, generations, mutation_rate,
                              selection, param, crossover, max_weight))
        results_general = [get_value_weight(ind, max_weight)[0] for ind in best_individuals]
        results_gen = [get_value_weight(ind, max_weight)[0] for ind in best_gen_individuals]
        best_value = get_value_weight(best_individual, max_weight)[0]
        axs[i, 0].plot(results_gen)
        axs[i, 0].set_title(f'Wartości najlepszego osobnika\npróba {i + 1}, najlepsza wartość {best_value}')
        axs[i, 0].set_xlabel('Generacja')
        axs[i, 0].set_ylabel('Wartość [zł]')
        axs[i, 1].plot(results_general)
        axs[i, 1].set_title(f'Wartości najlepszego osobnika dla aktualnej generacji\npróba {i + 1}, '
                            f'najlepsza wartość {best_value}', fontsize=10)
        axs[i, 1].set_xlabel('Generacja')
        axs[i, 1].set_ylabel('Wartość [zł]')
    plt.tight_layout()
    plt.show()


params1 = {'population_size': 2000,
           'generations': 500,
           'mutation_rate': 0.01,
           'selection': roulette_selection,
           'param': 0.8,
           'crossover': two_point_crossover,
           'max_weight': 6_404_180}

start(**params1)
# 13 692 887 dla 6 397 822
