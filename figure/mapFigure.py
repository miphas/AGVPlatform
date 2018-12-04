# -*- coding: UTF-8 -*-

# Import draw figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Import import other files
import sys
sys.path.append('..')

# Import setting and map2D
import setting as sett 
from map.map2D import Map2D

#
from sensor.radar2D import Radar2D
import math


class MapFigure:

    # MapFigure constructor
    def __init__(self, map):
        self.map = map
        self.fig, self.ax = plt.subplots()
    
    # __MapFigure init before drawing
    def __beforeDraw(self):
        plt.cla()
    
    # MapFigure draw map by using features
    def drawMapByFeatures(self, color = 'black'):
        self.__beforeDraw()
        mfs = self.map.s_features
        for i in range(len(mfs)):
            self.__addFeatureOnFig(mfs[i], color)
    
    # MapFigure draw map by using grids
    def drawMapByGrids(self, color = 'black'):
        self.__beforeDraw()
        grid = self.map.s_grid
        self.__traverseAllGrid(grid, self.__setGridColor, color=color)
    
    # MapFigure draw radar 
    def drawRadarPoints(self, xs, ys, style = 'ro', w = 1.0):
        l1, = plt.plot(xs, ys, style)
        l1.set_lw(w)
        return l1
    
    def drawErrorBar(self, x, y, err, f='k-o'):
        return self.ax.errorbar(x, y, yerr=err, fmt=f)
    
    # MapFigure add label on figure
    def setXYLabel(self, xLabel, yLabel):
        plt.xlabel(xLabel, fontproperties = sett.getChineseFont())
        plt.ylabel(yLabel, fontproperties = sett.getChineseFont())
    
    # MapFigure set x and y limit on figure
    def setXYLim(self, xlimA, xlimB, ylimA, ylimB):
        plt.xlim((xlimA, xlimB))
        plt.ylim((ylimA, ylimB))

    def setAspect(self, rate = 1):
        self.ax.set_aspect(rate)

    # MapFigure show the figure
    def showFigure(self):
        plt.show()

    def __getPathVal(self, points):
        x, y = points[0], points[1]
        w, h = points[2], points[3]
        angle = 0
        if len(points) > 4:
            angle = points[4]
        return x, y, w, h, angle
    # __MapFigure get rect
    def __getRectPath(self, points, color):
        x, y, w, h, angle = self.__getPathVal(points)
        return patches.Rectangle((x, y), w, h, angle, facecolor=color, edgecolor=color)
    
    def __getEllipsePath(self, points, color):
        x, y, w, h, angle = self.__getPathVal(points)
        return patches.Ellipse((x, y), w, h, angle, facecolor=color, edgecolor=color)
    
    # __MapFigure operate with all the grid
    def __traverseAllGrid(self, grid, func, **arg):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                func(grid, i, j, **arg)
    
    # __MapFigure set single grid's color
    def __setGridColor(self, grid, i, j, color):
        if grid[i][j] != 0:
            pa = self.__getRectPath([i, j, 1, 1], color)
            self.ax.add_patch(pa)
    
    # __MapFigure add feature on map
    def __addFeatureOnFig(self, feature, color):
        if feature.type == Map2D.Feature.rectangle:
            pa = self.__getRectPath(feature.points, color)
            self.ax.add_patch(pa)
        elif feature.type == Map2D.Feature.ellipse:
            pa = self.__getEllipsePath(feature.points, color)
            self.ax.add_patch(pa)
        elif feature.type == Map2D.Feature.erase:
            pa = self.__getRectPath(feature.points, 'white')
            self.ax.add_patch(pa)

# 画布基础测试
def __TestBasicDrawFunc():
    # create map
    map = Map2D(200, 200)
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [50, 50, 10, 20]))
    from map.objModel import ObjModel
    mdl = ObjModel([Map2D.Feature(Map2D.Feature.ellipse, [25, 25, 40, 30, 0])], 50, 50)
    #map2 = Map2D(50, 50)
    map2 = mdl.getRotateModel(30)
    print map2.m_width, map2.m_height
    #map2.addFeature(Map2D.Feature(Map2D.Feature.ellipse, [25, 25, 40, 30, 0]))
    map.addSubMap(map2, 0, 0)
    # create figure
    fig = MapFigure(map)
    # 2 types of drawing
    #fig.drawMapByFeatures()
    fig.drawMapByGrids() # This one is slow
    fig.setXYLim(0, 200, 0, 200)
    fig.showFigure()

# 激光雷达数据测试
def __TestRadarDrawFunc():
    # create map /mm
    map = Map2D(2000, 2000)
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [100, 500, 500, 1400]))
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [1400, 600, 600, 1200]))

    radar = Radar2D([0, math.pi], 510, 5600, 1, 5)
    radar_pos = radar.getMeasureData(map, [1000, 0, 0])

    fig = MapFigure(map)
    fig.drawMapByFeatures()
    fig.drawRadarPoints([x[0] for x in radar_pos], [x[1] for x in radar_pos], 'r.')
    fig.setXYLim(0, 2000, 0, 2000)
    fig.showFigure()

# 模型绘制测试
def __TestBasicDrawFunc():
    # create map
    map = Map2D(1500, 1000)
    from map.objModel import ObjModel
    from map.objModel import Models
    mdl = ObjModel(Models.carModel, 170, 375)

    m_car1 = mdl.getRotateModel(103)
    m_car2 = mdl.getRotateModel(87)

    map.addSubMap(m_car1, 0, 0)
    map.addSubMap(m_car2, 597, -20)
    # create figure
    fig = MapFigure(map)
    # 2 types of drawing
    #fig.drawMapByFeatures()

    fig.drawMapByGrids() # This one is slow
    fig.setXYLim(0, 1500, 0, 1000)
    fig.setAspect()

    from sensor.radar2D import Radar2D
    radar = Radar2D([0, math.pi], 510, 800, 1, 5)
    radar_pos = [600, 200, 0]
    radar_data = radar.getMeasureData(map, radar_pos)

    xs = [x[0] for x in radar_data]
    ys = [x[1] for x in radar_data]
    #print len(xs)
    for dat in radar_data:
        print dat[0], dat[1]
    fig.drawRadarPoints(xs, ys, 'r.')

    fig.showFigure()


if __name__ == '__main__':
    __TestBasicDrawFunc()
    #__TestRadarDrawFunc()