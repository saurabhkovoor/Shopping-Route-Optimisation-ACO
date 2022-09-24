import random
import numpy as np
# import math
import matplotlib.pyplot as plt

shop_list = [  # [x,y, name]
    [0, 0, "A"],
    [1, 1, "B"],
    [0, 2, "C"],
    [2, 0, "D"],
    [2, 2, "E"]
]

shop_list3 = [  # [x,y,category, name]
    [0, 0, "Halal Restaurant", "A"],
    [1, 1, "Luxury Clothing", "B"],
    [0, 2, "Normal Clothing", "C"],
    [2, 0, "Arcade", "D"],
    [2, 2, "Tech", "E"]
]

shop_list2 = {
    "s0": ["A", "Halal Restaurant", (0, 0)],
    "s1": ["B", "Luxury Clothing", (1, 1)],
    "s2": ["C", "Normal Clothing", "luxury", (0, 2)],
    "s3": ["D", "Arcade", (2, 0)],
    "s4": ["E", "Tech", (2, 2)]
}

entrance_exit = [
    [0, 1, "Exit A"]
]

entrance_exit2 = {
    "e0": ["Exit A", (0, 1)],
    "e1": ["Exit B", (6, 1)]
}


def create_graph(points):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    points_x = [point.coordinates[0] for key, point in points.items()]
    points_y = [point.coordinates[1] for key, point in points.items()]
    ax.scatter(points_x, points_y)
    ax.set_aspect(aspect=1.0)
    ax.invert_yaxis()
    return ax


def draw_pheromone(ax, paths):
    lines = []
    for path in paths:
        from_coord = path.connected_points[0].coordinates
        to_coord = path.connected_points[1].coordinates
        coord_x = [from_coord[0], to_coord[0]]
        coord_y = [from_coord[1], to_coord[1]]
        lines.append(ax.plot(coord_x, coord_y, c='k',
                     linewidth=path.pheromone**2))
    return lines


class Point:  # need to check again because this might be class for points, and not all points are shops
    def __init__(self, name, pheromone=0):  # add category
        self.name = name
        #self.category = category
        self.paths = []
        self.coordinates = []
        # self.pheromone = pheromone
        # self.cost = 1

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    # def get_coordinates(self):
    #     return self.coordinates

    def add_path(self, path):
        if path not in self.paths:
            self.paths.append(path)

    # def set_cost(self, cost):
    #     self.cost = cost

    # def calculate_cost(self, coordinates):
    #     self.cost = math.hypot(self.coordinates[0] - coordinates[0], self.coordinates[1] - coordinates[1])


class Path:
    def __init__(self, connected_points, cost=1, pheromone=0):
        self.connected_points = connected_points
        self.cost = cost
        #self.cost = cost
        # distance between two points
        #self.cost = math.hypot(connected_points[1][0] - connected_points[0][0], connected_points[1][1] - connected_points[0][1])
        #self.cost = sqrt( (connected_points[1][0] - connected_points[0][0])**2 + (connected_points[1][1] - connected_points[0][1])**2 )
        self.pheromone = pheromone

        def set_pheromone(self, pheromone):
            self.pheromone = pheromone

        # update the pheromone on the path
        def evaporate_pheromone(self, rho):
            self.pheromone *= (1-rho) * self.pheromone

        def deposit_pheromone(self, ants):
            deposited_pheromone = 0
            for ant in ants:
                if self in ant.road:
                    deposited_pheromone += 5/ant.get_road_length()**1
                    # deposited_pheromone += 5/ant.get_road_length()
            self.pheromone += deposited_pheromone

        def get_connected_points(self):
            return self.connected_points


class Ant:
    def __init__(self):
        self.points = []  # the sequence of points that the ant goes through
        self.road = []  # the sequence of paths that the and utilises

        def get_road(self, origin, destination, alpha):
            # appending the origin point to the self.points
            self.points.append(origin)
            # checking if the last point is not the destination then the search for the next point to travel to proceeds
            while self.points[-1] is not destination:
                if len(self.road) > 0:
                    available_paths = [
                        p for p in self.points[-1].paths if p is not self.road[-1]]
                else:
                    available_paths = self.points[-1].paths
                if len(available_paths) == 0:
                    available_paths = [self.road[-1]]
                pheromones_alpha = [p.pheromone **
                                    alpha for p in available_paths]
                probabilities = [pa/sum(pheromones_alpha)
                                 for pa in pheromones_alpha]
                acc_probabilities = [sum(probabilities[:i+1])
                                     for i, p in enumerate(probabilities)]
                chosen_value = random.random()

                for ai, ap in enumerate(acc_probabilities):
                    if ap > chosen_value:
                        break
                self.road.append(available_paths[ai])
                if self.road[-1].connected_points[0] is self.points[-1]:
                    self.points.append(self.road[-1].connected_points[1])
                else:
                    self.points.append(self.road[-1].connected_points[0])
            # removing loopy path
            while len(set(self.points)) != len(self.points):
                for i, point in enumerate(set(self.points)):
                    point_indices = [i for i, x in enumerate(
                        self.points) if x == point]
                    if len(point_indices) > 1:
                        self.points = self.points[:point_indices[0]
                                                  ] + self.points[point_indices[-1]:]
                        self.road = self.road[:point_indices[0]
                                              ] + self.road[point_indices[-1]:]
                        break

        def get_road_length(self):
            return sum([path.cost for path in self.road])

        def reset(self):
            self.points = []
            self.road = []


def get_frequency_of_roads(ants):
    roads = []
    points = []
    frequencies = []
    for ant in ants:
        if len(ant.road) != 0:
            if ant.road in roads:
                frequencies[roads.index(ant.road)] += 1
            else:
                roads.append(ant.road)
                points.append(ant.points)
                frequencies.append(1)
    return [frequencies, roads, points]


def get_percentage_of_dominant_road(ants):
    [frequencies, _, _] = get_frequency_of_roads(ants)
    if len(frequencies) == 0:
        percentage = 0
    else:
        percentage = max(frequencies)/sum(frequencies)
    return percentage


if __name__ == "__main__":
    points = {}

    grid = np.zeros([3, 3]) * -1
    a, b = grid.shape
    # print(a)
    # print(b)

    for x in range(a):
        for y in range(b):
            grid[x, y] = str(x) + str(y)
            points[str(x) + str(y)] = Point(str(x) + str(y))
            points[str(x) + str(y)].set_coordinates([x, y])

    paths = []

    # instantiating paths between cells (need to change 2 to a and b)
    for x in range(a):
        for y in range(b):
            # print(str(x)+str(y))
            if x != 2:  # horizontal direction
                path = Path(
                    [points[str(x)+str(y)], points[str(x + 1) + str(y)]])
                points[str(x)+str(y)].add_path(path)
                points[str(x + 1)+str(y)].add_path(path)
                paths.append(path)

            # print(str(x)+str(y))

            if y != 2:  # vertical direction
                path = Path(
                    [points[str(x)+str(y)], points[str(x) + str(y + 1)]])
                points[str(x)+str(y)].add_path(path)
                points[str(x)+str(y + 1)].add_path(path)
                paths.append(path)

            if (y != 2) and (x != 2):  # bottom-right diagonal direction
                path = Path(
                    [points[str(x)+str(y)], points[str(x + 1) + str(y + 1)]])
                points[str(x)+str(y)].add_path(path)
                points[str(x + 1)+str(y + 1)].add_path(path)
                paths.append(path)

            # upwards top-right diagonal direction
            if (x != 0) and (y != 2):
                path = Path(
                    [points[str(x)+str(y)], points[str(x - 1) + str(y + 1)]])
                points[str(x)+str(y)].add_path(path)
                points[str(x - 1) + str(y + 1)].add_path(path)
                paths.append(path)

    # print(path.get_connected_points("00"))

    origin = points["10"]
    destination = points["22"]
    n_ant = 10
    alpha = 1
    rho = 0.1
    initial_pheromone = 0.001

    for path in paths:
        # path.set_pheromone(initial_pheromone)
        path.pheromone = initial_pheromone

    ants = [Ant() for _ in range(n_ant)]

    # Termination criteria to end loop
    max_iteration = 200
    percentage_of_dominant_road = 0.9

    iteration = 0
    ax = create_graph(points)

    lines = draw_pheromone(ax, paths)
    while (iteration < max_iteration and get_percentage_of_dominant_road(ants) < percentage_of_dominant_road):
        # loop through all the ants to identify the path of each ant
        for ant in ants:
            # reset the path of the ant
            # ant.reset() # for some reason reset function not working, recognising as attribute
            ant.points = []
            ant.road = []

            # identify the path of the ant
            ant.get_road(origin, destination, alpha)

        # loop through all roads
        for path in paths:
            # evaporate the pheromone on the road
            path.evaporate_pheromone(rho)
            # deposit the pheromone
            path.deposit_pheromone(ants)
        # visualise
        for l in lines:
            del l
        lines = draw_pheromone(ax, paths)
        plt.pause(0.05)
        # increase iteration count
        iteration += 1

    # after exiting the loop, return the most occurred path as the solution
    [freq, roads, points_used] = get_frequency_of_roads(ants)
    print([p.name for p in points_used[freq.index(max(freq))]])
    input()

    # to set coordinates for shops
    # for coord1, coord2, name in shop_list:
    #     points[name] = Point(name)
    #     points[name].set_coordinates([coord1, coord2])

    # print(points["10"].get_coordinates())

    # for point1, point2, cost in step_cost:
    #   road = Road([cities[city1], cities[city2]], cost)
    #   cities[city1].add_road(road)
    #   cities[city2].add_road(road)
    #   roads.append(road)

    # for city1, city2, cost in step_cost:
    #   road = Road([cities[city1], cities[city2]], cost)
    #   cities[city1].add_road(road)
    #   cities[city2].add_road(road)
    #   roads.append(road)

    # origin = cities['Arad']
    # destination = cities['Bucharest']
