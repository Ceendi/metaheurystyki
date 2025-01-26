import matplotlib.pyplot as plt

from antcolony import AntColony
from customer import Customer
from twoopts import TwoOpt


def parse_file(filename):
    data = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.split()
            data.append(
                Customer(
                    int(line[0]),
                    float(line[1]),
                    float(line[2]),
                    float(line[3]),
                    float(line[4]),
                    float(line[5]),
                    float(line[6]),
                )
            )
    return data


if __name__ == "__main__":
    customers = parse_file("r101.txt")

    colony = AntColony(alpha=3, beta=1, capacity=200, customers=customers, evaporation_rate=0.1, iterations=200,
                       n_ants=300)

    twoopt = TwoOpt()

    best_path, best_dist = colony.run()

    x_coords = [customer.x for customer in best_path]
    y_coords = [customer.y for customer in best_path]

    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')

    plt.show()

    print(f"BEST DIST: {best_dist}")

    print(best_path)

    # optimized_path = twoopt.optimize(best_path)
    #
    # x_coords = [customer.x for customer in optimized_path]
    # y_coords = [customer.y for customer in optimized_path]
    #
    # plt.figure(figsize=(8, 6))
    # plt.scatter(x_coords, y_coords, color='blue', label='Punkty')
    # plt.plot(x_coords, y_coords, linestyle='-', color='gray', label='Linia między punktami')
    #
    # print(f"OPTIMIZED DIST: {twoopt.total_distance(optimized_path)}")
    #
    # plt.show()
