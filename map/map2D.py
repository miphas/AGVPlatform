# -*- coding: UTF-8 -*-

class Map2D:

    # Feature describe features in Map2D
    class Feature:
        # 2 types of feature
        ploygon = 'po'
        rectangle = 're'
        # Feature constructor
        def __init__(self, type, points):
            self.type = type
            self.points = points
    
    # Map2D constructor 
    def __init__(self, width, height, val = 0):
        # save the map's width and height
        self.m_width = width
        self.m_height = height
        # save the map with 2 types of ways
        self.s_grid = [([val] * height) for i in range(0, width)]
        self.s_features = []
    
    # Map2D add feature on map
    def addFeature(self, feature, val = 1):
        self.s_features.append(feature)
        if feature.type == Map2D.Feature.rectangle:
            x, y = feature.points[0], feature.points[1]
            w, h = feature.points[2], feature.points[3]
            self.__fillRect(x, y, w, h, val)
            

    # __Map2D check if point in map
    def __checkInMap(self, x, y):
        return 0 <= x and x < self.m_width and 0 <= y and y < self.m_height

    # __Map2D set value in map
    def __setValueInMap(self, x, y, val):
        if self.__checkInMap(x, y):
            self.s_grid[x][y] = val

    # __Map2D fill grid map
    def __fillRect(self, x, y, w, h, val):
        for i in range(0, w):
            for j in range(0, h):
                self.__setValueInMap(x + i, y + j, val)
    


'''
map = Map2D(50, 50)
print map.m_height, Map2D.Feature.ploygon
'''