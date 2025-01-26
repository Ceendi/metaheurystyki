import math
import random

from matplotlib import pyplot as plt


class TwoOpt:
    @staticmethod
    def calculate_distance(point1, point2):
        """Oblicza euklidesową odległość między dwoma punktami."""
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    def total_distance(self, route):
        """Oblicza całkowitą długość trasy."""
        distance = 0
        for i in range(len(route)):
            start_point = route[i]
            end_point = route[(i + 1) % len(route)]
            distance += self.calculate_distance(start_point, end_point)
        return distance

    @staticmethod
    def swap_2opt(route, i, k):
        """Wykonuje zamianę 2-opt, odwracając część trasy między indeksami i oraz k."""
        new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
        return new_route

    def optimize_2opt(self, route):
        """Optymalizuje trasę przy użyciu algorytmu 2-opt."""
        improved = True

        while improved:
            improved = False
            best_distance = self.total_distance(route)

            for i in range(1, len(route) - 1):
                for k in range(i + 1, len(route)):
                    new_route = self.swap_2opt(route, i, k)
                    new_distance = self.total_distance(new_route)

                    if new_distance < best_distance:
                        route = new_route
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break

        return route

    def optimize(self, route):
        new_points = [route[0]]
        temp_points = []
        for i in range(0, len(route)):
            temp_points.append(route[i])
            if route[i].x == route[0].x and route[i].y == route[0].y:
                temp_points = self.optimize_2opt(temp_points)
                # print(temp_points)
                new_points.extend(temp_points[1:])
                temp_points = [route[0]]
        # print(new_points)
        return new_points


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

    # new_points = [points[0]]
    # temp_points = []
    # for i in range(0, len(points)):
    #     temp_points.append(points[i])
    #     if points[i].x == 0 and points[i].y == 0:
    #         temp_points = twoo.optimize_2opt(temp_points)
    #         new_points.extend(temp_points[1:])
    #         temp_points = [points[0]]

    opt_points = twoo.optimize(points)



    print("Początkowa trasa:", [(p.x, p.y) for p in points])
    print("Długość początkowej trasy:", twoo.total_distance(points))
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]

    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')

    plt.show()

    print("Początkowa trasa:", [(p.x, p.y) for p in opt_points])
    print("Długość początkowej trasy:", twoo.total_distance(opt_points))
    x_coords = [point.x for point in opt_points]
    y_coords = [point.y for point in opt_points]

    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')

    plt.show()
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
