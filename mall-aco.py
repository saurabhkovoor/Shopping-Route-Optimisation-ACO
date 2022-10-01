import functions as F
import matplotlib.pyplot as plt
import numpy as np
import math
import time


location_list = [  #arranged by row
    [0, 0, "Uniqlo", "Clothing", ""],
    [1, 0, "1, 0", "-", ""],
    [2, 0, "Funscape Arcade", "Arcade", ""],
    [3, 0, "3, 0", "-", ""],
    [4, 0, "Machines", "Tech Store", ""],
    [5, 0, "5, 0", "-", ""],
    [6, 0, "Dominos Pizza", "Restaurant", ""],
    [0, 1, "Entrance / Exit A", "EE", ""],
    [1, 1, "Korean BBQ", "Restaurant", "Non-halal restaurant"],
    [2, 1, "2, 1", "-", ""],
    [3, 1, "Prada", "Clothing", "Luxury boutique"],
    [4, 1, "4, 1", "-", ""],
    [5, 1, "Pets At Home", "Pet Shop", "Pet shop"],
    [6, 1, "Entrance / Exit B", "EE", ""],
    [0, 2, "Borders Books", "Bookstore", ""],
    [1, 2, "1, 2", "-", ""],
    [2, 2, "Jaya Grocer", "Supermarket", ""],
    [3, 2, "3, 2", "-", ""],
    [4, 2, "Kyochon Chicken", "Restaurant", ""],
    [5, 2, "5, 2", "-", ""],
    [6, 2, "Cotton On", "Clothing", ""],
    ]
    
if __name__ == "__main__":
    plt.close('all')
    grid = np.zeros([7,3])
    nrow, ncol = grid.shape
    points = F.instantiatePoints(grid, location_list)
    paths = F.instantiatePaths(nrow, ncol, points)
    isMenuValid = False
    
    while not isMenuValid:
        menuInput = input("Enter menu selection: \n1 - Free travel (no constraints)\n2 - Fixed entrance and exit\n3 - Travel with constraints\n")
        try: 
            menuN = int(menuInput)
            if (menuN <= 0 or menuN > 3):
                raise ValueError
            else:                    
                if menuN == 1:
                    selectedShops, selectedShopNames = F.shopMenu(points)
                    start = time.time()
                    travelRoute, costs = F.travel(points, paths, selectedShops)
                    end = time.time()
                    print("\nPath")
                    for p in travelRoute:
                        if p in selectedShopNames:
                            print(f"\033[4m{p}\033[0m", end=" ~ ")
                        else:
                            print(p, end=" ~ ")
                    print("")
                    #rounding to 3 dp to avoid long float issue
                    print(f"Total Cost: {round(math.fsum(costs), 3)}")
                    print(f"Program execution time: {round((end - start), 3)}s")
                    isMenuValid = True
                    
                elif menuN == 2:
                    selectedShopNames, travelRoute, costs, duration = F.fixedEntExit(points, paths)
                    
                    print("\n\033[4mPath\033[0m")
                    for p in travelRoute:
                        if p in selectedShopNames:
                            print(f"\033[4m{p}\033[0m", end=" ~ ")
                        else:
                            print(p, end=" ~ ")
                    print("")
                    print(f"Total Cost: {round(math.fsum(costs), 3)}")
                    print(f"Program execution time: {round((duration), 3)}s")
                    isMenuValid = True
                    
                else:
                    selectedShopNames, travelRoute, costs, duration = F.withRestrictions(points, paths)
                    
                    print("\nPath")
                    for p in travelRoute:
                        if p in selectedShopNames:
                            print(f"\033[4m{p}\033[0m", end=" ~ ")
                        else:
                            print(p, end=" ~ ")
                    print("")
                    print(f"Total Cost: {round(math.fsum(costs),3)}")
                    print(f"Program execution time: {round((duration), 3)}s")
                    isMenuValid = True
                    
        except ValueError:
            print("Please enter a valid selection\n")