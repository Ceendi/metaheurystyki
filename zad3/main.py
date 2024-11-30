import math
import random
from collections import defaultdict
from matplotlib import pyplot as plt


def load_places_from_file(filename):
    places = []
    id_map = {}
    with open(filename) as f:
        for line in f:
            id_, x, y = list(map(int, line.strip().split(' ')))
            places.append((x, y))
            id_map[(x, y)] = id_
    return places, id_map


class AntColony:
    def __init__(self, n_ants, random_choice_probability, alpha, beta, iterations, evaporation_rate, places):
        self.n_ants = n_ants
        self.random_choice_probability = random_choice_probability
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations
        self.evaporation_rate = evaporation_rate
        self.places = places
        self.distances = self.calculate_distance()
        self.ant_colony: list[Ant] = []
        self.pheromones = defaultdict(lambda: defaultdict(lambda: 1.0))
        for place1 in places:
            for place2 in places:
                if place1 is not place2:
                    self.pheromones[place1][place2] = 1.0

    def update_pheromones(self):
        for place1 in self.places:
            for place2 in self.places:
                if place1 != place2:
                    self.pheromones[place1][place2] *= (1 - self.evaporation_rate)

        for ant in self.ant_colony:
            for place1, place2 in zip(ant.path[:-1], ant.path[1:]):
                self.pheromones[place1][place2] += 1 / ant.calculate_distance(self.distances)

    def calculate_distance(self):
        distances = defaultdict(lambda: defaultdict(float))
        for place1 in self.places:
            for place2 in self.places:
                dist = math.sqrt((place1[0] - place2[0]) ** 2 + (place1[1] - place2[1]) ** 2)
                if dist == 0:
                    dist = 1e-10
                distances[place1][place2] = dist
        return distances

    def run(self):
        best_path = None
        best_distance = float('inf')

        for _ in range(self.iterations):
            self.ant_colony = [Ant(random.choice(self.places)) for _ in range(self.n_ants)]
            for ant in self.ant_colony:
                places = self.places[:]
                places.remove(ant.current_position)

                for _ in range(len(self.places) - 1):  # -1 because we selected one at the start
                    if random.uniform(0, 1) < self.random_choice_probability:
                        ant.pick_random_path(places)
                    else:
                        ant.pick_path(self.pheromones, self.distances, places, self.alpha, self.beta)

                    places.remove(ant.current_position)

                distance = ant.calculate_distance(self.distances)
                if distance < best_distance:
                    best_distance = distance
                    best_path = ant.path

            self.update_pheromones()

        return best_path, best_distance


class Ant:
    def __init__(self, start):
        self.start = start
        self.current_position = start
        self.path = [start]

    def pick_path(self, pheromones, distances, places, alpha, beta):
        probabilities = []
        sum_ = sum((pheromones[self.current_position][place] ** alpha) *
                   (1 / distances[self.current_position][place] ** beta) for place in places)

        for place in places:
            prob = ((pheromones[self.current_position][place] ** alpha) *
                    (1 / distances[self.current_position][place] ** beta))
            probabilities.append(prob / sum_)

        picked_place = random.choices(places, weights=probabilities, k=1)[0]

        self.path.append(picked_place)
        self.current_position = picked_place

    def pick_random_path(self, places):
        random_place = random.choice(places)
        self.path.append(random_place)
        self.current_position = random_place

    def calculate_distance(self, distances) -> float:
        distance_sum = 0
        for location1, location2 in zip(self.path[:-1], self.path[1:]):
            distance_sum += distances[location1][location2]
        return distance_sum


def draw_path(path, id_map):
    x_coords, y_coords = zip(*path)
    print(x_coords, y_coords)

    plt.figure(figsize=(10, 6))
    plt.plot(x_coords + (x_coords[0],), y_coords + (y_coords[0],), marker='o', linestyle='-', color='b')

    for i, (x, y) in enumerate(path):
        plt.text(x, y, f'{id_map[(x, y)]}', fontsize=9, ha='right', va='bottom')

    plt.title('Path Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.axis('equal')
    plt.show()


def main():
    places, id_map = load_places_from_file('A-n80-k10.txt')
    colony = AntColony(500, 0.05, 2, 3, 100,
                       0.3, places)
    best_path, best_distance = colony.run()
    draw_path(best_path, id_map)
    print(f'shortest_distance: {best_distance}, best path: {best_path}')


if __name__ == '__main__':
    main()

# best 425.36162526086196 dla n32????
# best 754.6628643342029 dla n80????