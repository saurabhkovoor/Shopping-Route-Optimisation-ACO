import random
import numpy as np
import math
import matplotlib.pyplot as plt

shop_list = [ # [x,y, name]
    [0, 0, "A"],
    [1,1,"B"],
    [0,2,"C"],
    [2,0,"D"],
    [2,2,"E"]
]

shop_list3 = [ # [x,y,category, name]
    [0, 0, "Halal Restaurant", "A"],
    [1,1,"Luxury Clothing", "B"],
    [0,2,"Normal Clothing", "C"],
    [2,0,"Arcade", "D"],
    [2,2,"Tech", "E"]
]

shop_list2 = {
    "s0": ["A", "Halal Restaurant", (0,0)],
    "s1": ["B", "Luxury Clothing", (1,1)],
    "s2": ["C", "Normal Clothing", "luxury", (0,2)],
    "s3": ["D", "Arcade", (2,0)],
    "s4": ["E", "Tech", (2,2)]  
    }

entrance_exit = [
    [0,1,"Exit A"]
    ]

entrance_exit2 = {
    "e0": ["Exit A", (0,1)],
    "e1": ["Exit B", (6,1)]
    }

class Point: # need to check again because this might be class for points, and not all points are shops
    def __init__(self, name, pheromone = 0): # add category
        self.name = name
        #self.category = category
        self.paths = []
        self.coordinates = []
        self.pheromone = pheromone
        self.cost = 1
        
    def set_coordinates(self, coordinates):
        self.coordinates =  coordinates
        
    def get_coordinates(self):
        return self.coordinates
    
    def add_path(self, path):
        if path not in self.paths:
            self.paths.append(path)
    
    def set_cost(self, cost):
        self.cost = cost
        
    def calculate_cost(self, coordinates):
        self.cost = math.hypot(self.coordinates[0] - coordinates[0], self.coordinates[1] - coordinates[1])

        
class Path:
    def __init__(self, connected_points, pheromone=0):
        self.connected_points = connected_points
        self.cost = 1
        #self.cost = cost
        # distance between two points
        #self.cost = math.hypot(connected_points[1][0] - connected_points[0][0], connected_points[1][1] - connected_points[0][1])
        #self.cost = sqrt( (connected_points[1][0] - connected_points[0][0])**2 + (connected_points[1][1] - connected_points[0][1])**2 )
        self.pheromone = pheromone
        
        def set_pheromone(self, pheromone):
            self.pheromone = pheromone
            
class Ant:
    def __init__(self):
        self.points = [] # the sequence of points that the ant goes through
        self.road = [] # the sequence of paths that the and utilises
        ants = [Ant() for _ in range(n_ant)]
        
        def get_road(self, origin, destination, alpha):
            self.points.append(origin)
            while self.points[-1] != destination:
                if len(self.road) > 0:
                    available_paths = [r for r in self.points[-1].paths if r != self.road[-1]]
                else:
                    available_paths = self.points[-1].paths
            
            
        def get_road_length(self):
            
        def reset(self):
            self.points = []
            self.road = []
            
        
        
if __name__ == "__main__":
    points = {}
    
    grid = np.zeros([3,3]) * -1
    a, b = grid.shape
    print(a)
    print(b)
    
    for x in range(a):
        for y in range(b):
            grid[x,y] = str(x) + str(y)
            points[str(x) + str(y)] = Point(str(x) + str(y))
            points[str(x) + str(y)].set_coordinates([x,y])
            
    # for coord1, coord2, name in shop_list:
    #     points[name] = Point(name)
    #     points[name].set_coordinates([coord1, coord2])
    
    paths = []
    
    # instantiating paths between cells (need to change 2 to a and b)
    for x in range(a):
        for y in range(b):
            print(str(x)+str(y))
            if x != 2: # horizontal direction
                path = Path(points[str(x)+str(y)],points[str(x + 1) + str(y)])
                points[str(x)+str(y)].add_path(path)
                points[str(x + 1)+str(y)].add_path(path)
                paths.append(path)
            
            print(str(x)+str(y))

            if y != 2: # vertical direction
                path = Path(points[str(x)+str(y)],points[str(x) + str(y + 1)])
                points[str(x)+str(y)].add_path(path)
                points[str(x)+str(y + 1)].add_path(path)
                paths.append(path)
                
            if (y != 2) and (x != 2): # bottom-right diagonal direction
                path = Path(points[str(x)+str(y)],points[str(x + 1) + str(y + 1)])
                points[str(x)+str(y)].add_path(path)
                points[str(x + 1)+str(y + 1)].add_path(path)
                paths.append(path)
                
            # upwards top-right diagonal direction
            if (x != 0) and (y != 2):
                path = Path(points[str(x)+str(y)],points[str(x - 1) + str(y + 1)])
                points[str(x)+str(y)].add_path(path)
                points[str(x - 1) + str(y + 1)].add_path(path)
                paths.append(path)
    
    origin = points["10"]
    destination = points["22"]
    n_ant = 10
    alpha = 1
    rho = 0.1
    initial_pheromone = 0.001
    for path in paths:
        path.set_pheromone(initial_pheromone)
        
    
    # to set coordinates for shops    
    # for coord1, coord2, name in shop_list:
    #     points[name] = Point(name)
    #     points[name].set_coordinates([coord1, coord2])
    
    print(points["10"].get_coordinates())
    
    
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