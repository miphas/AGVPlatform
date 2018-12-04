# -*- coding: UTF-8 -*-

import sys
sys.path.append('..')

from figure.mapFigure import MapFigure
from map.map2D import Map2D
from xlab.basic import Feas,ExpSetting
from dataFactory.randomNum import RandomNum

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

'''
cur_map = ExpSetting.getBasicMap(1600,800,Feas.fea2)
fig = MapFigure(cur_map)
fig.drawMapByFeatures()
fig.setXYLim(0, 1600, 0, 900)
fig.setAspect()
fig.showFigure()
'''


def draw3Dsurface(x, y, z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y = np.meshgrid(x, y)
    #z = np.sqrt(x ** 2, y**2)
    # Plot the surface.
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
#draw3Dsurface(np.arange(0, 5, 0.1), np.arange(0, 5, 0.1), 0)

'''
w = 1600
h = 800
map = ExpSetting.getBasicMap(w, h, Feas.fea2)
prob_map = Map2D(w, h, 0.5)
for i in range(len(Feas.fea2)):
    f = Map2D.Feature(Map2D.Feature.rectangle, Feas.fea2[i])
    prob_map.genInitProb(f)
draw3Dsurface(np.arange(0, h, 1), np.arange(0, w, 1), prob_map.s_grid)

'''
xs = [[25, 825], [975, 1575]]
ys = [[25, 85], [235, 285], [435, 465], [615, 665], [815, 885]]


def genRandPos(x, y, w, h, num):
    ran1 = RandomNum.createRandom(num) * w + x
    ran2 = RandomNum.createRandom(num) * h + y
    return ran1, ran2

w = 1600
h = 900
map = ExpSetting.getBasicMap(w, h, Feas.fea2)
fig = MapFigure(map)
fig.drawMapByFeatures()
# 主通道
#ran1, ran2 = genRandPos(825, 25, 150, 850, 300)
# 搜索c
#ran1, ran2 = genRandPos(825, 210, 150, 100, 50)
# 
ran1, ran2 = genRandPos(825, 690, 150, 80, 50)
fig.drawRadarPoints(ran1, ran2, 'b.')
'''
for i in range (len(xs)):
    for j in range(len(ys)):
        ran1, ran2 = genRandPos(xs[i][0], ys[j][0], xs[i][1] - xs[i][0], ys[j][1] - ys[j][0], 120)
        fig.drawRadarPoints(ran1, ran2, 'b.')
'''

fig.setXYLim(0, 1600, 0, 900)
fig.setXYLabel(u'距离/cm', u'距离/cm')
fig.setAspect()
fig.showFigure()