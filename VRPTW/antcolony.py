import math
from collections import defaultdict

from customer import Customer
from ant import Ant


class AntColony:
    def __init__(self, n_ants, alpha, beta, iterations, evaporation_rate, customers, capacity):
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations
        self.evaporation_rate = evaporation_rate
        self.customers: list[Customer] = customers
        self.distances = self.calculate_distance()
        self.ant_colony: list[Ant] = []
        self.capacity = capacity
        self.pheromones = defaultdict(lambda: defaultdict(lambda: 1.0))
        for customer1 in customers:
            for customer2 in customers:
                if customer1 is not customer2:
                    self.pheromones[customer1.no][customer2.no] = 1.0

    def update_pheromones(self, best_ant):
        for customer1 in self.customers:
            for customer2 in self.customers:
                if customer1 != customer2:
                    self.pheromones[customer1.no][customer2.no] *= (1 - self.evaporation_rate)

        for customer1, customer2 in zip(best_ant.path[:-1], best_ant.path[1:]):
            self.pheromones[customer1.no][customer2.no] += 1 / best_ant.calculate_distance(self.distances)

        for ant in self.ant_colony:
            for customer1, customer2 in zip(ant.path[:-1], ant.path[1:]):
                self.pheromones[customer1.no][customer2.no] += 1 / ant.calculate_distance(self.distances)

    def calculate_distance(self):
        distances = defaultdict(lambda: defaultdict(float))
        for customer1 in self.customers:
            for customer2 in self.customers:
                dist = math.sqrt((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2)
                if dist == 0:
                    dist = 1e-10
                distances[customer1.no][customer2.no] = dist
        return distances

    def run(self):
        best_path = None
        best_distance = float('inf')

        for _ in range(self.iterations):
            self.ant_colony = [Ant(self.customers[0]) for _ in range(self.n_ants)]
            for ant in self.ant_colony:
                customers = self.customers[:]

                while True:
                    ant.pick_path(self.pheromones, self.distances, customers, self.alpha, self.beta, self.capacity)

                    if len(customers) == 1:
                        break

                    if ant.current_position != self.customers[0]:
                        customers.remove(ant.current_position)

                distance = ant.calculate_distance(self.distances)
                if distance < best_distance:
                    best_distance = distance
                    best_path = ant.path
                    print(_)
                    print(best_distance)

            best_ant = min(self.ant_colony, key=lambda a: a.calculate_distance(self.distances))
            self.update_pheromones(best_ant)

        return best_path, best_distance
