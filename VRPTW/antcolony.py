import math
import numpy as np
from customer import Customer
from ant import Ant
from concurrent.futures import ProcessPoolExecutor


class AntColony:
    def __init__(self, n_ants, alpha, beta, iterations, evaporation_rate, customers, capacity):
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations
        self.evaporation_rate = evaporation_rate
        self.customers: list[Customer] = customers
        self.ant_colony: list[Ant] = []
        self.capacity = capacity

        self.distances = self.calculate_distance()
        self.pheromones = np.ones((len(self.customers), len(self.customers)))

    def update_pheromones(self, ant_results, best_path, best_distance):
        self.pheromones *= (1 - self.evaporation_rate)

        if best_path is not None:
            elite_deposit = 2 * (1 / best_distance)
            for c1, c2 in zip(best_path[:-1], best_path[1:]):
                self.pheromones[c1.no, c2.no] += elite_deposit

        for distance, path in ant_results:
            pheromone_deposit = 1 / distance
            for customer1, customer2 in zip(path[:-1], path[1:]):
                self.pheromones[customer1.no, customer2.no] += pheromone_deposit

    def calculate_distance(self):
        num_customers = len(self.customers)
        distances = np.zeros((num_customers, num_customers), dtype=np.float32)

        for i in range(num_customers):
            for j in range(num_customers):
                if i != j:
                    dist = math.sqrt((self.customers[i].x - self.customers[j].x) ** 2 +
                                     (self.customers[i].y - self.customers[j].y) ** 2)
                    distances[i, j] = dist

        return distances

    def run(self):
        best_path = None
        best_distance = float('inf')

        with ProcessPoolExecutor() as executor:
            for _ in range(self.iterations):
                self.ant_colony = [Ant(self.customers[0]) for _ in range(self.n_ants)]

                futures = [executor.submit(self.run_ant, ant) for ant in self.ant_colony]
                results = [future.result() for future in futures]

                best_ant = min(results, key=lambda a: a[0])
                best_distance_iter = best_ant[0]

                if best_distance_iter < best_distance:
                    best_distance = best_distance_iter
                    best_path = best_ant[1]
                    print(f"Iteration: {_}, best_distance: {best_distance}")

                self.update_pheromones(results, best_path, best_distance)

        return best_path, best_distance

    def run_ant(self, ant):
        available_customers = self.customers[:]

        while True:
            ant.pick_path(self.pheromones, self.distances, available_customers, self.alpha, self.beta,
                          self.capacity)

            if len(available_customers) == 1:
                break

            if ant.current_position != self.customers[0]:
                available_customers.remove(ant.current_position)

        return ant.calculate_distance(self.distances), ant.path
