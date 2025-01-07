import numpy as np


class Particle:
    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.velocity = np.array([0, 0])
        self.best_pos = self.pos
        self.best_value = np.inf


def goldstein_price_function(x, y):
    return ((1 + (x + y + 1) ** 2 * (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2)) *
            (30 + (2 * x - 3 * y) ** 2 * (18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2)))


def himmelblaus_function(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def initialize_particles(particles_num, x_bounds, y_bounds):
    return [
        Particle(
            np.random.uniform(x_bounds[0], x_bounds[1]),
            np.random.uniform(y_bounds[0], y_bounds[1])
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

        global_best_pos, global_best_value = update_values(func, global_best_pos, global_best_value, particles)

    return global_best_pos, global_best_value


# print(particle_swarm_optimization(goldstein_price_function,
#                                   100,
#                                   100,
#                                   (-2, 2),
#                                   (-2, 2),
#                                   0.2,
#                                   0.4,
#                                   0.4
#                                   ))

print(particle_swarm_optimization(himmelblaus_function,
                                  100,
                                  100,
                                  (-5, 5),
                                  (-5, 5),
                                  0.2,
                                  0.4,
                                  0.4
                                  ))
