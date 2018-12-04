# -*- coding: UTF-8 -*-

# import files
import sys
sys.path.append('..')

import math
import numpy as np
import matplotlib.pyplot as plt

from figure.mapFigure import MapFigure
from map.map2D import Map2D
from sensor.radar2D import Radar2D
from algorithms.split import Split
from algorithms.avg import Avg, Normal
from algorithms.dbscan import DBSCAN
from algorithms.leastSquare import LeastSquare
from xlab.basic import ExpSetting

class BoxPoint:

    defa_val = math.log(1)
    print "def", defa_val
    occp_val = math.log(9)
    free_val = math.log(1.0 / 9)

    print occp_val, free_val

    # 
    def __init__(self, radar, radar_data, radar_pos, rang, next_p):
        self.radar_pos = radar_pos
        self.avgXY = Avg.getRadarAvg(radar_data, rang[0], rang[1])
        print self.avgXY
        self.dis = abs(self.avgXY[0] - radar_pos[0])
        #print self.dis
        self.p1 = self.__getYPos(radar, self.dis, rang[1] - 1)
        self.p2 = self.__getYPos(radar, self.dis, next_p)
        if self.p1 > self.p2:
            self.p1, self.p2 = self.p2, self.p1
        print self.p1, self.p2
        self.ll = [0.0] * (max(self.p1, self.p2) * 3)
        self.__updateLL(self.ll, self.p1, self.p2)
    
    def updatePos(self, radar, radar_data, radar_pos, p_a, p_b):
        self.radar_pos = radar_pos
        self.dis = abs(self.avgXY[0] - radar_pos[0])
        np1 = self.__getYPos(radar, self.dis, p_a)
        np2 = self.__getYPos(radar, self.dis, p_b)
        print np1, np2
        self.__updateLL(self.ll, np1, np2)
    
    def getCurtPos(self):
        probs = self.__getProb(self.ll)
        x_val = self.avgXY[0]
        y_val = self.__getVals(self.radar_pos[0], probs)
        return x_val, y_val

    def __getYPos(self, radar, dis, lineNum):
        return int(radar_pos[1] + dis * math.tan(radar.angles[0] + lineNum * radar.ang_step))
    
    def __addVals(self, ll, val, start, end):
        for i in range(start, end):
            ll[i] += val
    
    def __updateLL(self, ll, p1, p2):
        if p1 > p2:
            p1, p2 = p2, p1
        self.__addVals(ll, self.occp_val, p1, p2)
        self.__addVals(ll, self.free_val, 0, p1)
        self.__addVals(ll, self.free_val, p2, len(ll))
    
    def __getProb(self, ll):
        ret = [0] * len(ll)
        for i in range(len(ll)):
            ret[i] = 1 - 1.0 / (1 + math.pow(math.e, ll[i]))
        Normal.normalParam(ret, self.p1, self.p2)
        return ret
    
    def __getVals(self, start, probs):
        ret = 0.0
        for i in range(self.p1, self.p2):
            #print probs[i]
            ret += (start + i) * probs[i]
        return ret

# 实验1 角点 环境布局
def exp_jiao_environment():
    map = ExpSetting.getBasicMap()
    fig = MapFigure(map)
    fig.drawMapByFeatures()
    fig.setXYLabel(u'距离/mm', u'距离/mm')
    fig.setXYLim(0, 2500, 0, 3200)
    fig.showFigure()
#exp_jiao_environment()

# 实验1 角点 雷达数据
def exp_jiao_radardata(radar_pos):
    map = ExpSetting.getBasicMap()
    fig = MapFigure(map)
    radar = ExpSetting.getBasicRadar()
    radar_data = radar.getMeasureData(map, radar_pos)
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    colors = ['b.', 'r.', 'g.']
    xs = [x[0] for x in radar_data]
    ys = [x[1] for x in radar_data]
    for i in range(len(rag)):
        s = rag[i][0]
        e = rag[i][1]
        fig.drawRadarPoints(xs[s : e], ys[s : e], colors[i])
    fig.setXYLabel(u'距离/mm', u'距离/mm')
    fig.setXYLim(0, 2500, 0, 3200)
    fig.showFigure()
#exp_jiao_radardata([0,0,0])
#exp_jiao_radardata([500, 1000, 0])

# 实验1 角点 实际数据
def exp_jiao_drawErrRange():
    dats = [[1977, 2007], [1982, 2012], [1993, 2002], [1979, 2006], [1994, 2023],
            [1992, 2016], [1992, 2015], [1996, 2017], [1983, 2003], [1996, 2014]]
    x = np.arange(1, 11, 1)
    y = []
    e = []
    for i in range(len(dats)):
        y.append((dats[i][0] + dats[i][1]) / 2.0)
        e.append(dats[i][1] - y[i])
    
    map = ExpSetting.getBasicMap()
    fig = MapFigure(map)
    fig.drawErrorBar(x, y, e, 'k-o')
    fig.drawRadarPoints(np.arange(0, 12), [2000] * 12, 'r--')
    fig.setXYLabel(u'数据编号', u'距离/mm')
    fig.setXYLim(0, 11, 1950, 2050)
    fig.showFigure()
#exp_jiao_drawErrRange()

# 实验1 角点 估计位置

def exp_jiao_drawEstimate(p1, p2, p3, y1, y2):
    xs = np.arange(1, 11)
    map = ExpSetting.getBasicMap()
    fig = MapFigure(map)
    l1 = fig.drawRadarPoints(xs, p3, 'ro-')
    l2 = fig.drawRadarPoints(xs, p1, 'g--<')
    l3 = fig.drawRadarPoints(xs, p2, 'm:d')
    plt.legend([l1, l2, l3], [u'AAAAA', u'B', 'C'], loc = 'upper right')
    fig.setXYLabel(u'数据编号', u'距离/mm')
    fig.setXYLim(0, 11, y1, y2)
    fig.showFigure()

# 角点数据
'''
p1 = [1991.50, 1992.62, 1994.00, 1993.21, 1994.14,
        1995.84, 1998.21, 1998.90, 1998.32, 1999.00]
p2 = [1977, 1982, 1992, 1992, 1993,
        1993, 1994, 1996, 1996, 1996]
p3 = [2000] * 10
exp_jiao_drawEstimate(p1, p2, p3, 1950, 2050)
'''
# 边缘数据
'''
p1 = [2046, 2003, 2051, 2059, 2081, 2092, 2094, 2098, 2099, 2100]
p2 = [2043, 2007, 2045, 2056, 2077, 2081, 2085, 2094, 2096, 2098]
p3 = [2100] * 10
exp_jiao_drawEstimate(p1, p2, p3, 1950, 2150)
'''
# 边缘角度
'''
p1 = [0.052, 0.093, 0.046, 0.038, 0.0087,
      0.023, 0.0022, 0.0028, 0.0032, 0.00044]
p2 = [0.055, 0.090, 0.053, 0.041, 0.022,
      0.018, 0.0014, 0.0032, 0.0044, 0.00044]
p3 = [0] * 10
for i in range(len(p1)):
    p1[i] = math.atan2(p1[i], 1.0)
    p2[i] = math.atan2(p2[i], 1.0)
print p1
print p2
exp_jiao_drawEstimate(p1, p2, p3, -0.5, 0.5)
'''
def drawP_val(x_vals, y_vals):
    fig, ax = plt.subplots()
    # 去除上侧、右侧框
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    # 设置坐标值只在下方显示
    ax.xaxis.set_ticks_position('bottom')
    # 不显示默认坐标
    plt.xticks([])
    plt.yticks([])
    # 画标准距离、最大距离
    ax.set_xticks([2, 8])
    ax.set_xticklabels(['y1', 'y2'])
    # 设置x、y的极限值
    plt.xlim((0, 12))
    plt.ylim((0, 0.45))
    # 画出曲线
    plt.plot(x_vals, y_vals)
    from figure.setting import getChineseFont
    #plt.xlabel(u'测量距离', fontproperties=getChineseFont())
    plt.ylabel(u'P(y)', fontproperties=getChineseFont())
    plt.show()
'''
p_val = [0] * 12
for i in range(2, 9):
    p_val[i] = 0.1
drawP_val(np.arange(2, 9), [0.03] * 7)
'''

'''
def calNum(k):
    param = (k - 1) / 0.1
    val9 = 2.0 / (9.0 * (k - 1))
    lval = math.pow(1.0 - val9 + 2.35 * math.sqrt(val9), 3.0)
    return param * lval
for i in range(2, 50):
    print calNum(i)
'''


def drawMeasurePoint(radar_data, rag, p = [0, 0]):
    # 绘图
    xs = [x[0] for x in radar_data]
    ys = [x[1] for x in radar_data]

    fig = MapFigure(map)
    fig.drawMapByFeatures()

    colors = ['b.', 'r.', 'g.','b.', 'r.', 'g.','b.', 'r.', 'g.']
    for i in range(len(rag)):
        s = rag[i][0]
        e = rag[i][1]
        fig.drawRadarPoints(xs[s : e], ys[s : e], colors[i])
    
    fig.drawRadarPoints([p[0]], [p[1]], 'wo')

    fig.setXYLim(0, 2000, 0, 3000)
    fig.showFigure()

def getGroupData(radar, map, radar_pos, r_idx):
    radar_data = radar.getMeasureData(map, radar_pos)
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    mid = Split.getSingleSplitPoint(radar_data, rag[r_idx])
    return [radar_pos, radar_data, rag, mid]

def getRadarData(start, end, step, r_idx):
    # 创建地图、增加两个货包块
    map = ExpSetting.getBasicMap()
    radar = ExpSetting.getBasicRadar()

    ret = []
    ret.append(getGroupData(radar, map, [0, 0, 0], r_idx))
    for i in range(start, end, step):
        ret.append(getGroupData(radar, map, [500, i, 0], 1))
    return ret






def estimateLine():
    # 创建地图、增加两个货包块
    map = ExpSetting.getBasicMap()

    # 创建激光雷达、设置位置、扫描数据
    radar = ExpSetting.getBasicRadar()
    radar_pos = [0, 0, 0]
    radar_data = radar.getMeasureData(map, radar_pos)

    # 获取
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    mid = Split.getSingleSplitPoint(radar_data, rag[0])

    theta, p_val = LeastSquare.normalCal(radar_data, rag[0][0], mid - 3)
    ls = LeastSquare(theta, p_val)

    for i in range(5, 700, 70):
        radar_pos = [i, 0, 0]
        radar_data = radar.getMeasureData(map, radar_pos)
        rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
        print rag
        mid = Split.getSingleSplitPoint(radar_data, rag[0])
        print ls.recursiveCal(radar_data, rag[0][0], mid - 3)

def estimateLine2():
    # 创建地图、增加两个货包块
    map = ExpSetting.getBasicMap()

    # 创建激光雷达、设置位置、扫描数据
    radar = ExpSetting.getBasicRadar()
    radar_pos = [0, 0, 0]
    radar_data = radar.getMeasureData(map, radar_pos)

    # 获取
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    mid = Split.getSingleSplitPoint(radar_data, rag[1])

    theta, p_val = LeastSquare.normalCal(radar_data, rag[1][0], mid - 2)
    ls = LeastSquare(theta, p_val)

    for i in range(1000, 2000, 100):
        radar_pos = [500, i, 0]
        radar_data = radar.getMeasureData(map, radar_pos)
        rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
        print rag
        mid = Split.getSingleSplitPoint(radar_data, rag[1])
        print ls.recursiveCal(radar_data, rag[1][0], mid - 5, 0.98)

def estimateLine3(dat, rate = 1.0):
    

    theta, p_val = LeastSquare.normalCal(dat[0][1], dat[0][2][1][0], dat[0][3] - 2)
    ls = LeastSquare(theta, p_val)

    for i in range(1, len(dat)):
        theta, p_val = ls.recursiveCal(dat[i][1], dat[i][2][1][0], dat[i][3] - 5, rate)
        print theta


if __name__ == '__main__':
    '''
    #drawErrRange()
    dat = getRadarData(1000, 2000, 100, 1)
    print 
    estimateLine3(dat, 1.0)
    estimateLine3(dat, 0.95)
    '''


'''
    map = ExpSetting.getBasicMap()

    # 创建激光雷达、设置位置、扫描数据
    radar = ExpSetting.getBasicRadar()
    radar_pos = [500, 1900, 0]
    radar_data = radar.getMeasureData(map, radar_pos)

    # 获取
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    print rag
    mid = Split.getSingleSplitPoint(radar_data, rag[1])

    drawMeasurePoint(radar_data, rag, [radar_data[mid][0], radar_data[mid][1]])
'''

'''
    # 创建地图、增加两个货包块
    map = ExpSetting.getBasicMap()

    # 创建激光雷达、设置位置、扫描数据
    radar = ExpSetting.getBasicRadar()
    radar_pos = [0, 0, 0]
    radar_data = radar.getMeasureData(map, radar_pos)

    # 获取
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    print rag
    mid = Split.getSingleSplitPoint(radar_data, rag[0])
    #print mid
    drawMeasurePoint(radar_data, rag)

    LeastSquare.normalCal(radar_data, rag[0][0], mid - 3)
    for i in range(mid + 1, rag[0][1]):
        radar_data[i][0] += i - mid
    LeastSquare.normalCal(radar_data, mid + 1, rag[0][1])
'''

'''
    boxPoint = BoxPoint(radar, radar_data, radar_pos, [mid + 1, rag[0][1]], rag[1][0])
    print boxPoint.getCurtPos()

    for i in range(5, 700, 70):
        radar_pos = [0, i, 0]
        radar_data = radar.getMeasureData(map, radar_pos)
        rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
        print rag
        mid = Split.getSingleSplitPoint(radar_data, rag[0])
        boxPoint.updatePos(radar, radar_data, radar_pos, rag[1][0] - 1, rag[1][0])
        print i, boxPoint.getCurtPos()
'''


'''

    print boxPoint.getCurtPos()


    # 绘图
    xs = [x[0] for x in radar_data]
    ys = [x[1] for x in radar_data]

    fig = MapFigure(map)
    fig.drawMapByFeatures()

    colors = ['b.', 'r.', 'g.']
    for i in range(len(rag)):
        s = rag[i][0]
        e = rag[i][1]
        fig.drawRadarPoints(xs[s : e], ys[s : e], colors[i])


    fig.setXYLim(0, 2000, 0, 3000)
    fig.showFigure()
'''

import matplotlib.pyplot as plt
import numpy.random as rnd
from matplotlib.patches import Ellipse
import matplotlib.patches

NUM = 250

ells = [Ellipse(xy=rnd.rand(2)*10, width=rnd.rand(), height=rnd.rand(), angle=rnd.rand()*360)
        for i in range(NUM)]
e = Ellipse((0, 0), width=30, height=40, angle=0, facecolor='black')

fig, ax = plt.subplots()
#ax = plt.subplots()#fig.add_subplot(111, aspect='equal')
#for e in ells:
ax.add_patch(e)
    #ax.add_artist(e)
    #e.set_clip_box(ax.bbox)
    #e.set_alpha(rnd.rand())
    #e.set_facecolor(rnd.rand(3))

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

plt.show()

