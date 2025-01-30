import matplotlib.pyplot as plt

from antcolony import AntColony
from customer import Customer


def parse_file(filename):
    data = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.split()
            data.append(
                Customer(
                    int(line[0]) - 1,
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

    params = {
        'alpha': 1.5,
        'beta': 1,
        'capacity': 200,
        'customers': customers,
        'evaporation_rate': 0.4,
        'iterations': 100,
        'n_ants': 100
    }

    fig, axes = plt.subplots(3, 2, figsize=(12, 16))
    axes = axes.flatten()
    results = []

    for i in range(6):
        colony = AntColony(**params)
        best_path, best_dist = colony.run()
        results.append(best_dist)

        depot = customers[0]
        split_indices = [i for i, customer in enumerate(best_path) if customer == depot]
        routes = [best_path[start:end + 1] for start, end in zip(split_indices, split_indices[1:])]

        ax = axes[i]
        x_coords = [c.x for c in best_path]
        y_coords = [c.y for c in best_path]

        ax.scatter(x_coords, y_coords, color='blue', alpha=0.5)
        ax.scatter([depot.x], [depot.y], color='red', marker='s', s=50, zorder=3)

        colors = plt.cm.tab20.colors
        for veh_id, route in enumerate(routes):
            path_x = [c.x for c in route]
            path_y = [c.y for c in route]
            ax.plot(path_x, path_y, color=colors[veh_id % len(colors)], linewidth=2, label=f'Pojazd {veh_id+1}')

            ax.set_title(
                f"Liczba pojazdów: {len(routes)}\nDystans: {best_dist:.2f}",
                fontsize=10
            )
        ax.set_aspect('auto')
        ax.margins(0.05)

    fig.suptitle(
        f"Parametry: alpha={params['alpha']}, beta={params['beta']}, "
        f"capacity={params['capacity']}, evaporation_rate={params['evaporation_rate']}, "
        f"iterations={params['iterations']}, n_ants={params['n_ants']}\n"
        f"średni={sum(results) / len(results):.2f}, max={max(results):.2f}, min={min(results):.2f}",
        fontsize=14,
        y=0.95
    )

    plt.show()
