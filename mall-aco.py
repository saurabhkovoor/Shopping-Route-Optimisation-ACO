import random
import numpy as np
import matplotlib.pyplot as plt

store_list = [  #arranged by row
    [0, 0, "Uniqlo", "Clothing", ""],
    [2, 0, "Funscape Arcade", "Arcade", ""],
    [4, 0, "Machines", "Tech Store", ""],
    [6, 0, "Dominos Pizza", "Restaurant", ""],
    [1, 1, "Korean BBQ", "Restaurant", "non-halal"],
    [3, 1, "Prada", "Clothing", "luxury"],
    [5, 1, "Pets At Home", "Pet Shop", "Pet Shop"],
    [0, 2, "Borders Books", "Bookstore", ""],
    [2, 2, "Jaya Grocer", "Supermarket", ""],
    [4, 2, "Kyochon Chicken", "Restaurant", ""],
    [6, 2, "Cotton On", "Clothing", ""],
    ]


# shop_list3 = [  # [x,y,category, name]
#     [0, 0, "Halal Restaurant", "A"],
#     [1, 1, "Luxury Clothing", "B"],
#     [0, 2, "Normal Clothing", "C"],
#     [2, 0, "Arcade", "D"],
#     [2, 2, "Tech", "E"]
# ]

# shop_list2 = {
#     "s0": ["A", "Halal Restaurant", (0, 0)],
#     "s1": ["B", "Luxury Clothing", (1, 1)],
#     "s2": ["C", "Normal Clothing", "luxury", (0, 2)],
#     "s3": ["D", "Arcade", (2, 0)],
#     "s4": ["E", "Tech", (2, 2)]
# }

# entrance_exit = [
#     [0, 1, "Exit A"]
# ]

# entrance_exit2 = {
#     "e0": ["Exit A", (0, 1)],
#     "e1": ["Exit B", (6, 1)]
# }


def create_graph(points):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    points_x = [point.coordinates[0] for key, point in points.items()]
    points_y = [point.coordinates[1] for key, point in points.items()]
    ax.scatter(points_x, points_y)
    ax.set_aspect(aspect=1.0)
    ax.invert_yaxis()
    
    for i, (key, value) in enumerate(points.items()):
        remark = f" *{value.tag}" if value.tag != "" else ""
        label = f"{key}\n{value.category}{remark}"
        ax.annotate(label, (points_x[i], points_y[i]))
    
    return ax


def draw_pheromone(ax, paths):
    lines = []
    for path in paths:
        from_coord = path.connected_points[0].coordinates
        to_coord = path.connected_points[1].coordinates
        coord_x = [from_coord[0], to_coord[0]]
        coord_y = [from_coord[1], to_coord[1]]
        lines.append(ax.plot(coord_x, coord_y, c='k',
                     linewidth=path.pheromone**(1/5)))
    return lines


class Point:  # need to check again because this might be class for points, and not all points are shops
    def __init__(self, name, pheromone=0):  # add category
        self.name = name
        self.paths = []
        self.coordinates = []
        self.category = ""
        self.tag = ""

    def set_coordinates(self, coordinates): 
        self.coordinates = coordinates
        
        
    def set_category_tag(self, category, tag):
        self.category = category
        self.tag = tag

    def add_path(self, path):
        if path not in self.paths:
            self.paths.append(path)
            
    # def calculate_cost(self, coordinates):
    #     self.cost = math.hypot(self.coordinates[0] - coordinates[0], self.coordinates[1] - coordinates[1])


class Path:
    def __init__(self, connected_points, cost=1, pheromone=0):
        self.connected_points = connected_points
        self.cost = cost
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
                deposited_pheromone += 1/ant.get_road_length()
        self.pheromone += deposited_pheromone
        
    def set_cost(self, cost):
        self.cost = cost


class Ant:
    def __init__(self):
        self.points = []  # the sequence of points that the ant goes through
        self.road = []  # the sequence of paths that the and utilises

    def get_road(self, origin, destination, alpha):
        # appending the origin point to the self.points
        self.points.append(origin)
        
        # checking if the last point is not the destination then the search for the next point to travel to proceeds
        recent_point = self.points[-1]
        while recent_point != destination:
            connected_paths = recent_point.paths
    
            pheromone_sum_w_alpha = sum([path.pheromone * alpha for path in connected_paths]) # can make this power of alpha
            probabilities_ls = [(alpha * path.pheromone) / pheromone_sum_w_alpha for path in connected_paths]
            selectedPath = random.choices(population=connected_paths, weights=probabilities_ls)[0]
            if selectedPath.connected_points[0] == recent_point:
                recent_point = selectedPath.connected_points[1]
            else:
                recent_point = selectedPath.connected_points[0]
            
            self.points.append(recent_point)
            self.road.append(selectedPath)
            
        # removing loopy path after reaching destination, by removing loops/repeated points within existing path (self.cities)
        # the points and the corresponding paths between the repetition will be removed
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
    plt.close('all')
    points = {}

    grid = np.zeros([7,3])
    nrow, ncol = grid.shape
    paths = []
      
    for x, y, name, category, tag in store_list:
        points[name] = Point(name)
        points[name].set_coordinates([x,y])
        points[name].set_category_tag(category, tag)
        grid[x,y] = str(x) + str(y) #check
        

    pointDict = points.copy()
    
    
    for key, val in points.items():
        pointDict.pop(key)  #doesnt draw again
        currentX = val.coordinates[0]
        currentY = val.coordinates[1]
        horizontalPoints = [i for i in pointDict if pointDict[i].coordinates[1] == currentY]
        verticalPoints = [i for i in pointDict if pointDict[i].coordinates[0] == currentX]
        btDiagonals = [i for i in pointDict if pointDict[i].coordinates[0] == currentX+1 and pointDict[i].coordinates[1] == currentY+1]
        trDiagonals = [i for i in pointDict if pointDict[i].coordinates[0] == currentX-1 and pointDict[i].coordinates[1] == currentY+1]
        
        #horizontal direction 
        if currentX < nrow:   
            for p in horizontalPoints:
                # path = Path(
                #         [str(currentX)+str(currentY) , str(points[p].coordinates[0])+str(points[p].coordinates[1])])
                path = Path(
                        [points[key] , points[p]])
                points[key].add_path(path)
                points[p].add_path(path)
                paths.append(path)
                
        #vertical direction
        if currentY < ncol:   
            for p in verticalPoints:
                # path = Path(
                #         [str(currentX)+str(currentY) , str(points[p].coordinates[0])+str(points[p].coordinates[1])])
                path = Path(
                        [points[key] , points[p]])
                points[key].add_path(path)
                points[p].add_path(path)
                paths.append(path)
            
        # bottom-right diagonal direction
        if currentX < nrow and currentY < ncol:
            for p in btDiagonals:
                # path = Path([str(currentX)+str(currentY), str(points[p].coordinates[0])+str(points[p].coordinates[1])], 1.412)
                path = Path(
                        [points[key] , points[p]], 1.412)
                points[key].add_path(path)
                points[p].add_path(path)
                paths.append(path)
       
        #top-right diagonal direction
        if currentX != 0 and currentY < ncol:
            for p in trDiagonals:
                # path = Path([str(currentX)+str(currentY), str(points[p].coordinates[0])+str(points[p].coordinates[1])], 1.412)
                path = Path(
                        [points[key] , points[p]], 1.412)
                points[key].add_path(path)
                points[p].add_path(path)
                paths.append(path)



    origin = points["Uniqlo"]
    destination = points["Prada"]
    
    n_ant = 10
    alpha = 1
    rho = 0.1
    initial_pheromone = 0.001

    for path in paths:
        path.set_pheromone(initial_pheromone)

    ants = [Ant() for _ in range(n_ant)]

    # Termination criteria to end loop
    max_iteration = 100
    percentage_of_dominant_road = 0.9

    iteration = 0
    ax = create_graph(points)

    lines = draw_pheromone(ax, paths)
    while ((iteration < max_iteration) and (get_percentage_of_dominant_road(ants) < percentage_of_dominant_road)):
        print("Iteration: {0}\tPercentage: {1}".format(iteration, get_percentage_of_dominant_road(ants)))
        # looping through ants to find each ant's path
        
        for ant in ants:
            # reset the path of the ant
            ant.reset()

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
        plt.pause(2) # lower to make it faster
        # increase iteration count
        iteration += 1

    # after exiting the loop, return the most occurred path as the solution
    [freq, roads, points_used] = get_frequency_of_roads(ants)
    print([p.name for p in points_used[freq.index(max(freq))]])
    plt.show()



