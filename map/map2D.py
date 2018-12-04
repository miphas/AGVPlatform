# -*- coding: UTF-8 -*-

import numpy as np

class Map2D:

    # Feature describe features in Map2D
    class Feature:
        # 2 types of feature
        ploygon = 'po'
        ellipse = 'el'
        rectangle = 're'
        erase = 'era'
        # Feature constructor
        def __init__(self, type, points):
            self.type = type
            self.points = points
    
    unknown = 0
    occupied = 1

    # Map2D constructor 
    def __init__(self, width, height, val = unknown):
        # save the map's width and height
        self.m_width = width
        self.m_height = height
        # save the map with 2 types of ways
        #self.s_grid = [([val] * height) for i in range(0, width)]
        #self.s_grid = np.zeros((width, height))
        self.s_grid = np.array([val] * (width * height)).reshape((width, height))
        self.s_features = []
    
    # Map2D add feature on map
    def addFeature(self, feature, val = occupied):
        self.s_features.append(feature)
        x, y, w, h = self.__getFeaVal(feature.points)
        if feature.type == Map2D.Feature.rectangle:
            self.__fillRect(x, y, w, h, val)
        elif feature.type == Map2D.Feature.ellipse:
            self.__fillEllp(x, y, w, h, val)
        elif feature.type == Map2D.Feature.erase:
            self.__fillRect(x, y, w, h, self.unknown)
            pass
    
    def addSubMap(self, map, x, y, val = occupied):
        for i in range(0, map.m_width):
            for j in range(0, map.m_height):
                self.__maxValueInMap(x + i, y + j, map.s_grid[i][j])

    def genInitProb(self, feature):
        x, y = feature.points[0], feature.points[1]
        w, h = feature.points[2], feature.points[3]
        self.__fillAround(x, y, w, h)

    # Map2D check if point in map
    def checkInMap(self, x, y):
        return 0 <= x and x < self.m_width and 0 <= y and y < self.m_height

    def setValInMap(self, x, y, val):
        if self.checkInMap(x, y):
            self.s_grid[x][y] = val

    def __getFeaVal(self, points):
        x, y = points[0], points[1]
        w, h = points[2], points[3]
        return x, y, w, h

    # __Map2D set value in map
    def __setValueInMap(self, x, y, val):
        if self.checkInMap(x, y):
            self.s_grid[x][y] = val
    def __updateValueInMap(self, x, y, val):
        if self.checkInMap(x, y):
            self.s_grid[x][y] = min(self.s_grid[x][y], val)
    def __maxValueInMap(self, x, y, val):
        if self.checkInMap(x, y):
            self.s_grid[x][y] = max(self.s_grid[x][y], val)

    # __Map2D fill grid map
    def __fillRect(self, x, y, w, h, val):
        for i in range(0, w):
            for j in range(0, h):
                self.__setValueInMap(x + i, y + j, val)

    def __fillEllp(self, x, y, w, h, val):
        a = w / 2
        b = h / 2
        for i in range(-a, a + 1):
            for j in range(-b, b + 1):
                a2, b2, x2, y2 = a ** 2, b ** 2, i ** 2, j ** 2
                if b2 * x2 + a2 * y2 <= a2 * b2:
                    self.__setValueInMap(x + i, y + j, val)
    
    def __fillAround(self, x, y, w, h):
        vals = [0] * 25
        vals[21], vals[22], vals[23], vals[24] = 0, 0.1, 0.2, 0.4
        # 上下重新设置
        for i in range(0, w):
            for j in range(0, 25):
                self.__updateValueInMap(x + i, y - j - 1, vals[j])
                self.__updateValueInMap(x + i, y + h + j, vals[j])
        # 左右重新设置
        for i in range(0, 25):
            for j in range(0, h):
                self.__updateValueInMap(x - h - 1, y + j, vals[i])
                self.__updateValueInMap(x + w + h, y + j, vals[i])
        # 设置四角
        for i in range(0, 25):
            for j in range(0, 25):
                cur_val = vals[min(i, j)]
                self.__updateValueInMap(x - i - 1, y - j - 1, cur_val)
                self.__updateValueInMap(x + w + i, y + h + j, cur_val)
                self.__updateValueInMap(x - i - 1, y + h + j, cur_val)
                self.__updateValueInMap(x + w + i, y + j - 1, cur_val)

    

if __name__ == '__main__':
    map = Map2D(50, 50)
    print map.m_height, Map2D.Feature.ploygon, Map2D.unknown

