import random
import numpy as np
import matplotlib.pyplot as plt
import math

location_list = [  #arranged by row
    [0, 0, "Uniqlo", "Clothing", ""],
    [1, 0, "1, 0", "-", ""],
    [2, 0, "Funscape Arcade", "Arcade", ""],
    [3, 0, "3, 0", "-", ""],
    [4, 0, "Machines", "Tech Store", ""],
    [5, 0, "5, 0", "-", ""],
    [6, 0, "Dominos Pizza", "Restaurant", ""],
    [0, 1, "Entrance / Exit A", "EE", ""],
    [1, 1, "Korean BBQ", "Restaurant", "non-halal"],
    [2, 1, "2, 1", "-", ""],
    [3, 1, "Prada", "Clothing", "luxury"],
    [4, 1, "4, 1", "-", ""],
    [5, 1, "Pets At Home", "Pet Shop", "Pet Shop"],
    [6, 1, "Entrance / Exit B", "EE", ""],
    [0, 2, "Borders Books", "Bookstore", ""],
    [1, 2, "1, 2", "-", ""],
    [2, 2, "Jaya Grocer", "Supermarket", ""],
    [3, 2, "3, 2", "-", ""],
    [4, 2, "Kyochon Chicken", "Restaurant", ""],
    [5, 2, "5, 2", "-", ""],
    [6, 2, "Cotton On", "Clothing", ""],
    ]

def instantiatePoints(grid):
    points = {}
    for x, y, name, category, tag in location_list:
        points[name] = Point(name)
        points[name].set_coordinates([x,y])
        points[name].set_category_tag(category, tag)
        grid[x,y] = str(x) + str(y) 
    return points

def instantiatePaths(nrow, ncol, points):
    paths = []
    for x in range(nrow):
        for y in range(ncol):
            currentPoint = [i for i in points if points[i].coordinates[0] == x and points[i].coordinates[1] == y]
            #nrow-1 and ncol-1 = avoid border Points
            if x < (nrow-1):    #Horizontal direction
                nextHoriPoint = [i for i in points if points[i].coordinates[0] == x+1 and points[i].coordinates[1] == y]
                path = Path([points[currentPoint[0]], points[nextHoriPoint[0]]])
                points[currentPoint[0]].add_path(path)
                points[nextHoriPoint[0]].add_path(path)
                paths.append(path)
                
            if y < (ncol-1):    #Vertical direction
                nextVertiPoint = [i for i in points if points[i].coordinates[1] == y+1 and points[i].coordinates[0] == x]
                path = Path([points[currentPoint[0]], points[nextVertiPoint[0]]])
                points[currentPoint[0]].add_path(path)
                points[nextVertiPoint[0]].add_path(path)
                paths.append(path)
                
            if y < (ncol-1) and x < (nrow-1):   #Bottom right diagonal
                nextbrPoint = [i for i in points if points[i].coordinates[0] == x+1 and points[i].coordinates[1] == y+1]
                path = Path([points[currentPoint[0]], points[nextbrPoint[0]]],1.412)
                points[currentPoint[0]].add_path(path)
                points[nextbrPoint[0]].add_path(path)
                paths.append(path)
                
            if x != 0 and y < (ncol-1):     #Top right diagonal
                nexttrPoint = [i for i in points if points[i].coordinates[0] == x-1 and points[i].coordinates[1] == y+1]
                path = Path([points[currentPoint[0]], points[nexttrPoint[0]]],1.412)
                points[currentPoint[0]].add_path(path)
                points[nexttrPoint[0]].add_path(path)
                paths.append(path)
    return paths

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
                    self.points = self.points[:point_indices[0]] + self.points[point_indices[-1]:]
                    self.road = self.road[:point_indices[0]] + self.road[point_indices[-1]:]
                    # print(self.points)
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

def create_graph(points):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    middlePoints = [point.coordinates for point in points.values() if point.category == "-"]
    entranceExitPoints = [point.coordinates for point in points.values() if point.category == "EE"]   
    e_x, e_y = [p[0] for p in entranceExitPoints], [p[1] for p in entranceExitPoints]
    points_x = [point.coordinates[0] for point in points.values() if point.coordinates not in entranceExitPoints and point.coordinates not in middlePoints]
    points_y = [point.coordinates[1] for point in points.values() if point.coordinates not in entranceExitPoints and point.coordinates not in middlePoints]

    ax.scatter(points_x, points_y, marker = '^')
    ax.scatter(e_x, e_y, marker = 'x', color='r')
    ax.set_aspect(aspect=1.0)
    ax.invert_yaxis()
    ax.set_yticks(points_y)
    
    #plot store and exit points only
    shopPoints = [point.name for point in points.values() if point.coordinates not in entranceExitPoints and point.coordinates not in middlePoints]
    epoints = [point.name for point in points.values() if point.category == "EE"]
    
    for i, p in enumerate(shopPoints):
        remark = f" *{points[p].tag}" if points[p].tag != "" else ""
        label = f"{p}\n({points[p].category}){remark}"
        ax.annotate(label, (points_x[i], points_y[i]))
    
    for i, p in enumerate(epoints):
        ax.annotate(points[p].name, (e_x[i], e_y[i]))
    
    return ax

def aco(points, paths, origin, destination, costs):
    n_ant = 5 #initially was 10
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
# =============================================================================
#     ax = create_graph(points)
#     lines = draw_pheromone(ax, paths)
# =============================================================================
    while ((iteration < max_iteration) and (get_percentage_of_dominant_road(ants) < percentage_of_dominant_road)):
        print("Iteration: {0}\tPercentage: {1}".format(iteration, get_percentage_of_dominant_road(ants)))
        # looping through ants to find each ant's path
        for ant in ants:
            ant.reset()
            ant.get_road(origin, destination, alpha)

        # loop through all roads
        for path in paths:
            path.evaporate_pheromone(rho)
            path.deposit_pheromone(ants)
# =============================================================================
#         # visualise
#         for l in lines:
#             del l
#         lines = draw_pheromone(ax, paths)
#         plt.pause(2) # lower to make it faster
# =============================================================================
        # increase iteration count
        iteration += 1

    # after exiting the loop, return the most occurred path as the solution
    [freq, roads, points_used] = get_frequency_of_roads(ants)
    travelRoute = [p.name for p in points_used[freq.index(max(freq))]]
    plt.show()

    cost = 0
    for g in roads:
        for r in g:
            cost += r.cost
    print(f"path cost: {cost}")
    costs.append(cost)
    return travelRoute

def validateInput():
    isInputValid = False 
    while not isInputValid:
        try: 
            inputString = set(map(int, input().split(",")))
            assert len(inputString) >= 5
            #stores selected Point object
            selectedShops = [points[s] for i, s in enumerate(shops) if i in inputString]   
            selectedShops.sort(key=lambda x: x.coordinates[0])
            selectedShopNames = [s.name for s in selectedShops]
            print("\n\033[4mSelected shops\033[0m")
            for i in selectedShopNames:
                print(i)
            print("")
            isInputValid = True
        except ValueError:
                print("Please enter shop number only\n")
        except AssertionError:
            print("Please enter at least 5 shops\n")
    return selectedShops, selectedShopNames

def freeTravel(points, paths):
    selectedShops, selectedShopNames = validateInput()
    inFirstHalf = all(x.coordinates[0] <= 3 for x in selectedShops) #returns true or false
    inSecondHalf = all(x.coordinates[0] >= 3 for x in selectedShops)
    travelRoute = []
    costs = []
    
    if not inFirstHalf and not inSecondHalf: #in both halves - enter from A, exit from B - user travels from left to right of mall
        entrance = points["Entrance / Exit A"]
        ex = points["Entrance / Exit B"]
    elif inFirstHalf:
        entrance = points["Entrance / Exit A"]  
        ex = entrance
        nextNearest = selectedShops.pop(1)
        selectedShops.append(nextNearest)
    else:   #inSecondHalf
        entrance = points["Entrance / Exit B"]
        ex = entrance
        selectedShops.reverse()
        nextNearest = selectedShops.pop(1)
        selectedShops.append(nextNearest)
    
    selectedShops.insert(0, entrance)
    selectedShops.append(ex)
    travelRoute = []
    for i in range(len(selectedShops) - 1):
        route = aco(points, paths, selectedShops[i], selectedShops[i+1], costs)
        if i < (len(selectedShops) - 2):
            route.pop(-1)
        travelRoute.extend(route)  

    return selectedShopNames, travelRoute, costs

def rearrange(n, selectedShops, rearrangedShops):
    for i in range(n):
        closestVal = 6
        availableShops = [x for x in selectedShops if x not in rearrangedShops]
        if i == 0:  
            #list is already sorted
            #place first value closest to entrance / exit 
            #place second closest value at the back (wrap around)
            rearrangedShops[i] = selectedShops[i]
            rearrangedShops[n-1] = selectedShops[1]
        elif i < math.floor(n/2):
            prevValue = rearrangedShops[i-1].coordinates[0]
            rearrangedShops[i] = getClosestShop(availableShops, closestVal, prevValue) 
            
            availableShops = [x for x in selectedShops if x not in rearrangedShops]
            
            #From the back
            closestVal = 6
            nextValue = rearrangedShops[n-i].coordinates[0]
            rearrangedShops[n-1-i] = getClosestShop(availableShops, closestVal, nextValue) 
        elif i == math.floor(n/2) and n % 2 != 0:
            rearrangedShops[i] = availableShops[0] 
    return rearrangedShops

def getClosestShop(availableShops, closestVal, prevNext):
    for s in availableShops:
        value = s.coordinates[0]
        if abs(prevNext - value) < closestVal:
            closestVal = abs(prevNext - value)
            closestShop = s
    return closestShop

def fixedEntExit(points, paths):
    selectedShops, selectedShopNames = validateInput()
    print("\n\033[4mSelect one as your entrance and exit:\033[0m")
    print("*enter A or B")
    entranceExit = [e for e, val in points.items() if val.category == "EE"]
    for e in entranceExit:
        print(f"{e[-1]} - {e}")
    print("")
    isEntExitValid = False
    while not isEntExitValid:
        eeInput = input()
        try:
            userInput = str(eeInput)
            if (userInput.upper() not in ["A", "B"]):
                raise ValueError 
            else:
                n = len(selectedShops)
                rearrangedShops = [""]*n 
                travelRoute = []
                costs = []
                if userInput.upper() == "A":   
                    entExit = points["Entrance / Exit A"]
                    shopArrangement = rearrange(n, selectedShops, rearrangedShops)
                else:
                    entExit = points["Entrance / Exit B"]
                    selectedShops.reverse()
                    shopArrangement = rearrange(n, selectedShops, rearrangedShops)
                    
                shopArrangement.insert(0, entExit)
                shopArrangement.append(entExit)
                travelRoute = []
                for i in range(len(selectedShops) - 1):
                    route = aco(points, paths, shopArrangement[i], shopArrangement[i+1], costs)
                    if i < (len(shopArrangement) - 2):
                        route.pop(-1)
                    travelRoute.extend(route)  
                isEntExitValid = True
        except ValueError:
            print("Please enter a valid selection\n")
            
    return selectedShopNames, travelRoute, costs

if __name__ == "__main__":
    plt.close('all')
    grid = np.zeros([7,3])
    nrow, ncol = grid.shape
    points = instantiatePoints(grid)
    paths = instantiatePaths(nrow, ncol, points)
    isMenuValid = False
    
    while not isMenuValid:
        menuInput = input("Enter menu selection: \n1 - Free travel (no constraints)\n2 - Fixed entrance and exit\n3 - Travel with constraints\n")
        try: 
            menuN = int(menuInput)
            if (menuN <= 0 or menuN > 3):
                raise ValueError
            else:
                print("\n\033[4mPlease enter at least 5 shops to visit:\033[0m")
                print("*enter shop number separated by commas")
                shops = [p for p, val in points.items() if val.category != "EE" and val.category != "-"]
                for i, p in enumerate(shops):
                    print(f"{i} - {p}")
                    
                if menuN == 1:
                    selectedShopNames, travelRoute, costs = freeTravel(points, paths)
                    print("\nPath")
                    for p in travelRoute:
                        if p in selectedShopNames:
                            print(f"\033[4m{p}\033[0m", end=" ~ ")
                        else:
                            print(p, end=" ~ ")
                    print("")
                    print(f"Total Cost: {math.fsum(costs)}")
                    isMenuValid = True
                elif menuN == 2:
                    selectedShopNames, travelRoute, costs = fixedEntExit(points, paths)
                    print("\nPath")
                    for p in travelRoute:
                        if p in selectedShopNames:
                            print(f"\033[4m{p}\033[0m", end=" ~ ")
                        else:
                            print(p, end=" ~ ")
                    print("")
                    print(f"Total Cost: {math.fsum(costs)}")
                    isMenuValid = True
                    
        except ValueError:
            print("Please enter a valid selection\n")
    
