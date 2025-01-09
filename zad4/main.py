import numpy as np
from matplotlib import pyplot as plt, ticker
from matplotlib.colors import LogNorm


custom_colors = [
    "#FF0000",
    "#FF7F00",
    "#FF1493",
    "#FFFFFF",
    "#B0B0B0",
    "#8B4513",
    "#40E0D0",
    "#000000",
    "#98FF98",
]


class Particle:
    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.velocity = np.array([0, 0])
        self.best_pos = self.pos
        self.best_value = np.inf

    def enforce_bounds(self, x_bounds, y_bounds):
        self.pos[0] = np.clip(self.pos[0], min(x_bounds), max(x_bounds))
        self.pos[1] = np.clip(self.pos[1], min(y_bounds), max(y_bounds))


class Goldstein_Price:
    x_bounds = (-2, 2)
    y_bounds = (-2, 2)

    @staticmethod
    def func(x, y):
        return ((1 + (x + y + 1) ** 2 * (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2)) *
                (30 + (2 * x - 3 * y) ** 2 * (18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2)))


class Himmelblaus:
    x_bounds = (-5, 5)
    y_bounds = (-5, 5)

    @staticmethod
    def func(x, y):
        return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def initialize_particles(particles_num, x_bounds, y_bounds):
    return [
        Particle(
            np.random.uniform(min(x_bounds), max(x_bounds)),
            np.random.uniform(min(y_bounds), max(y_bounds))
        )
        for _ in range(particles_num)
    ]


def update_values(func, global_best_pos, global_best_value, particles):
    for particle in particles:
        value = func(*particle.pos)

        if value < global_best_value:
            global_best_value = value
            global_best_pos = particle.pos

        if value < particle.best_value:
            particle.best_value = value
            particle.best_pos = particle.pos
    return global_best_pos, global_best_value


def particle_swarm_optimization(func, particles_num, iterations, x_bounds, y_bounds, inertia, cog_coeff, soc_coeff):
    particles = initialize_particles(particles_num, x_bounds, y_bounds)

    global_best_pos = None
    global_best_value = np.inf

    global_best_pos, global_best_value = update_values(func, global_best_pos, global_best_value, particles)

    for i in range(iterations):
        for particle in particles:
            ine = inertia * particle.velocity
            cog = cog_coeff * (particle.best_pos - particle.pos)
            soc = soc_coeff * (global_best_pos - particle.pos)
            particle.velocity = ine + cog + soc
            particle.pos += particle.velocity

            particle.enforce_bounds(x_bounds, y_bounds)

        global_best_pos, global_best_value = update_values(func, global_best_pos, global_best_value, particles)

    return global_best_pos, global_best_value


def run(particles_num, iterations, inertia, cog_coeff, soc_coeff):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

    for j, type_ in enumerate([Goldstein_Price, Himmelblaus]):
        x = np.linspace(min(type_.x_bounds), max(type_.x_bounds), 200)
        y = np.linspace(min(type_.y_bounds), max(type_.y_bounds), 200)

        X, Y = np.meshgrid(x, y)
        Z = type_.func(X, Y)

        levels = np.logspace(np.log10(np.min(Z)), np.log10(np.max(Z)), 100)

        cs = axs[j].contourf(X, Y, Z, levels=levels, cmap='viridis', norm=LogNorm())

        cbar = fig.colorbar(cs, ax=axs[j])
        cbar.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda q, _: f'{q:.1e}'))

        for i in range(9):
            best_pos, best_value = particle_swarm_optimization(type_.func, particles_num, iterations, type_.x_bounds,
                                                               type_.y_bounds, inertia, cog_coeff, soc_coeff)

            axs[j].scatter(best_pos[0], best_pos[1], color=custom_colors[i], marker='o',
                           label=f'({','.join([str(np.round(x, 2)) for x in best_pos])}) = {best_value:.2f}')

        axs[j].set_xlabel('X')
        axs[j].set_ylabel('Y')
        axs[j].set_title(f'{type_.__name__}, granice x = {type_.x_bounds}, granice y = {type_.y_bounds}')
        axs[j].legend()

    plt.suptitle(
        f'liczba czasteczek={particles_num}, iteracji={iterations} inercja={inertia}, komponent poznawczy={cog_coeff}, '
        f'komponent spoleczny={soc_coeff}')
    plt.tight_layout()
    plt.show()


params = {
    "particles_num": 100,
    "iterations": 100,
    "inertia": 0.075,
    "cog_coeff": 0.8,
    "soc_coeff": 0.125
}

if __name__ == '__main__':
    run(**params)
