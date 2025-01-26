import random


class Ant:
    def __init__(self, start):
        self.start = start
        self.current_position = start
        self.path = [start]
        self.time = 0.0
        self.weight = 0.0

    def pick_path(self, pheromones, distances, customers, alpha, beta, capacity):
        customers = [customer for customer in customers[:] if customer is not self.current_position]

        valid_customers = [
            customer for customer in customers
            if self.weight + customer.demand <= capacity
               and self.time <= customer.due_date
               and customer is not self.start
        ]

        if not valid_customers:
            picked_customer = self.start
            self.time = 0
            self.weight = 0
        else:
            probabilities = []
            sum_prob = 0

            for customer in valid_customers:
                pheromone_value = pheromones[self.current_position.no][customer.no] ** alpha
                distance_value = (1 / distances[self.current_position.no][customer.no]) ** beta
                time_penalty = 1.003 ** (max(0, customer.due_date - self.time))
                capacity_penalty = 1.001 ** (max(0, capacity - (self.weight + customer.demand)))
                probability = pheromone_value * distance_value * (1 / (1 + time_penalty + capacity_penalty))
                probabilities.append(probability)
                sum_prob += probability

            probabilities = [prob / sum_prob for prob in probabilities]

            if random.random() < 0.02:
                picked_customer = random.choice(valid_customers)
            else:
                picked_customer = random.choices(valid_customers, weights=probabilities, k=1)[0]

        self.weight += picked_customer.demand
        if self.time < picked_customer.ready_time:
            self.time = picked_customer.ready_time + picked_customer.service_time
        else:
            self.time += picked_customer.service_time
        self.path.append(picked_customer)
        self.current_position = picked_customer

    def pick_random_path(self, customers):
        random_customer = random.choice(customers)
        self.path.append(random_customer)
        self.current_position = random_customer

    def calculate_distance(self, distances) -> float:
        distance_sum = 0
        for location1, location2 in zip(self.path[:-1], self.path[1:]):
            distance_sum += distances[location1.no][location2.no]

        return distance_sum
