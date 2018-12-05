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
    # 首先创建一个200x200地图
    map = Map2D(200, 200)
    # 地图中添加一个矩形
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [50, 50, 10, 20]))
    # 创建一个50x50的另一个地图
    map2 = Map2D(50, 50)
    # 添加椭圆特征
    map2.addFeature(Map2D.Feature(Map2D.Feature.ellipse, [25, 25, 40, 30, 0]))
    # map融合map2，把map2放到0，0位置
    map.addSubMap(map2, 0, 0)
    # 以下是画图部分
    fig = MapFigure(map)
    fig.drawMapByGrids() # This one is slow
    fig.setXYLim(0, 200, 0, 200)
    fig.showFigure()

# 激光雷达数据测试
def __TestRadarDrawFunc():
    # 创建一个大地图
    map = Map2D(2000, 2000)
    # 添加两个矩形障碍物
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [100, 500, 500, 1400]))
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [1400, 600, 600, 1200]))
    # 创建雷达类&&获取位置点
    radar = Radar2D([0, math.pi], 510, 5600, 1, 5)
    radar_pos = radar.getMeasureData(map, [1000, 0, 0])
    # 绘制地图
    fig = MapFigure(map)
    fig.drawMapByFeatures()
    fig.drawRadarPoints([x[0] for x in radar_pos], [x[1] for x in radar_pos], 'r.')
    fig.setXYLim(0, 2000, 0, 2000)
    fig.showFigure()

# 模型绘制测试
def __TestModelDrawFunc():
    # 创建一个大地图
    map = Map2D(1500, 1000)
    # 引入模型类以及模型
    from map.objModel import ObjModel
    from map.objModel import Models
    # 获取汽车模型
    mdl = ObjModel(Models.carModel, 170, 375)
	# 创建两个角度不同的汽车
    m_car1 = mdl.getRotateModel(103)
    m_car2 = mdl.getRotateModel(87)
	# 将车加入地图中
    map.addSubMap(m_car1, 0, 0)
    map.addSubMap(m_car2, 597, -20)
    # 创建画板
    fig = MapFigure(map)
	# 使用栅格绘制模型图
    fig.drawMapByGrids() # This one is slow
    fig.setXYLim(0, 1500, 0, 1000)
    fig.setAspect()
	# 获取传感器数据
    from sensor.radar2D import Radar2D
    radar = Radar2D([0, math.pi], 510, 800, 1, 5)
    radar_pos = [600, 200, 0]
    radar_data = radar.getMeasureData(map, radar_pos)
    # 解析数据
    xs = [x[0] for x in radar_data]
    ys = [x[1] for x in radar_data]
    # 画在图上
    for dat in radar_data:
        print dat[0], dat[1]
    fig.drawRadarPoints(xs, ys, 'r.')
	# 展示模型图
    fig.showFigure()


if __name__ == '__main__':
    # __TestBasicDrawFunc()
    __TestRadarDrawFunc()
    # __TestModelDrawFunc()