class TwoOpt:
    def optimize(self, route, distances):
        new_points = [route[0]]
        temp_points = [route[0]]
        for i in range(1, len(route)):
            temp_points.append(route[i])
            if route[i].x == route[0].x and route[i].y == route[0].y:
                temp_points = self.two_opt_vrptw(temp_points, distances)
                new_points.extend(temp_points[1:])
                temp_points = [route[0]]
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
