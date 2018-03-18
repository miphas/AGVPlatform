# -*- coding: UTF-8 -*-

# Import draw figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Import import other files
import sys
sys.path.append('..')

# Import setting and map2D
import Setting as sett 
from map.map2D import Map2D


class MapFigure:

    # MapFigure constructor
    def __init__(self, map):
        self.map = map
        self.fig, self.ax = plt.subplots()

    # MapFigure draw map by using features
    def drawMapByFeatures(self, color = 'black'):
        plt.cla()
        mfs = self.map.s_features
        for i in range(len(mfs)):
            self.__addFeatureOnFig(mfs[i], color)
    
    # MapFigure add label on figure
    def setXYLabel(self, xLabel, yLabel):
        plt.xlabel(xlabel, fontproperties = sett.getChineseFont())
        plt.ylabel(ylabel, fontproperties = sett.getChineseFont())
    
    # MapFigure set x and y limit on figure
    def setXYLim(self, xlimA, xlimB, ylimA, ylimB):
        plt.xlim((xlimA, xlimB))
        plt.ylim((ylimA, ylimB))

    # MapFigure show the figure
    def showFigure(self):
        plt.show()

    # __MapFigure
    def __getRectPath(self, points, color):
        x, y = points[0], points[1]
        w, h = points[2], points[3]
        return patches.Rectangle((x, y), w, h, facecolor=color)
    
    # __MapFigure
    def __addFeatureOnFig(self, feature, color):
        if feature.type == Map2D.Feature.rectangle:
            pa = self.__getRectPath(feature.points, color)
            self.ax.add_patch(pa)

map = Map2D(50, 100)
map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [0, 0, 200, 100]))


fig = MapFigure(map)
fig.drawMapByFeatures()
fig.setXYLim(0, 200, 0, 200)
fig.showFigure()