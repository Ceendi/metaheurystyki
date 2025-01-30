import math
import random

from matplotlib import pyplot as plt


class TwoOpt:
    def optimize(self, route, distances):
        new_points = [route[0]]
        temp_points = [route[0]]
        for i in range(1, len(route)):
            temp_points.append(route[i])
            # route[0].x == route[0].x and route[0].y == route[0].y
            if route[i].x == route[0].x and route[i].y == route[0].y:
                temp_points = self.two_opt_vrptw(temp_points, distances)
                # print(temp_points)
                new_points.extend(temp_points[1:])
                temp_points = [route[0]]
        # print(new_points)
        return new_points

    def two_opt_vrptw(self, route, distances):
        best_route = route.copy()
        best_cost = self.calculate_distance(distances, route)
        improvement = True

        while improvement:
            improvement = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    new_route = route[:i] + route[i:j+1][::-1] + route[j + 1:]
                    if self.is_feasible(new_route):
                        new_cost = self.calculate_distance(distances, new_route)
                        if new_cost < best_cost:
                            best_route = new_route
                            best_cost = new_cost
                            improvement = True
                            break
                if improvement:
                    break
            route = best_route
        return route

    def is_feasible(self, route):
        current_time = 0
        previous_customer = route[0]
        for customer in route[1:]:
            travel_time = previous_customer.service_time
            arrival_time = current_time + travel_time
            if arrival_time > customer.due_date:
                return False
            current_time = max(arrival_time, customer.ready_time)
            previous_customer = customer
        return True

    def calculate_distance(self, distances, path) -> float:
        distance_sum = 0
        for location1, location2 in zip(path[:-1], path[1:]):
            distance_sum += distances[location1.no, location2.no]

        return distance_sum



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    # Przykładowe punkty (obiekty Point)

    point0 = Point(0, 0)
    points1 = [
        point0,
        Point(-1, 3),
        Point(1, 5),
        Point(-1, 5),
        Point(1, 3),
        point0,
        Point(3, 1),
        Point(5, -1),
        Point(5, 1),
        Point(3, -1),
        point0,
        Point(-1, -3),
        Point(1, -5),
        Point(-1, -5),
        Point(1, -3),
        point0
    ]

    points = [Point(random.uniform(-10, 10), random.uniform(-10, 10)) for i in range(20)]
    points[0] = Point(0, 0)
    points[6] = Point(0, 0)
    points[12] = Point(0, 0)
    points[19] = Point(0, 0)

    twoo = TwoOpt()


    tablica = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    new_tablice = tablica[:3] + tablica[3:6 + 1][::-1] + tablica[6 + 1:]

    print(new_tablice)


    # new_points = [points[0]]
    # temp_points = []
    # for i in range(0, len(points)):
    #     temp_points.append(points[i])
    #     if points[i].x == 0 and points[i].y == 0:
    #         temp_points = twoo.optimize_2opt(temp_points)
    #         new_points.extend(temp_points[1:])
    #         temp_points = [points[0]]

    # opt_points = twoo.optimize(points)
    #
    #
    #
    # print("Początkowa trasa:", [(p.x, p.y) for p in points])
    # print("Długość początkowej trasy:", twoo.total_distance(points))
    # x_coords = [point.x for point in points]
    # y_coords = [point.y for point in points]
    #
    # plt.figure(figsize=(8, 6))
    # plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    # plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')
    #
    # plt.show()
    #
    # print("Początkowa trasa:", [(p.x, p.y) for p in opt_points])
    # print("Długość początkowej trasy:", twoo.total_distance(opt_points))
    # x_coords = [point.x for point in opt_points]
    # y_coords = [point.y for point in opt_points]
    #
    # plt.figure(figsize=(8, 6))
    # plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    # plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')
    #
    # plt.show()
    #
    # Początkowa losowa trasa
    # initial_route = points[:]
    # random.shuffle(initial_route)

    # x_coords = [point.x for point in initial_route]
    # y_coords = [point.y for point in initial_route]
    #
    # plt.figure(figsize=(8, 6))
    # plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    # plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')
    #
    # plt.show()

    # print("Początkowa trasa:", [(p.x, p.y) for p in initial_route])
    # print("Długość początkowej trasy:", twoo.total_distance(initial_route))

    # Optymalizacja trasy
    # optimized_route = twoo.optimize_2opt(initial_route)

    # x_coords = [point.x for point in optimized_route]
    # y_coords = [point.y for point in optimized_route]
    #
    # plt.figure(figsize=(8, 6))
    # plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    # plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')
    #
    # print("Optymalna trasa:", [(p.x, p.y) for p in optimized_route])
    # print("Długość optymalnej trasy:", twoo.total_distance(optimized_route))
    #
    # plt.show()
