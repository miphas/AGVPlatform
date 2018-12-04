# -*- coding: UTF-8 -*-

# import files
import sys
sys.path.append('..')
import math

from figure.mapFigure import MapFigure
from map.map2D import Map2D
from sensor.radar2D import Radar2D
from algorithms.split import Split
from algorithms.avg import Avg, Normal
from algorithms.dbscan import DBSCAN


class Feas:
    fea1 = [[1000, 1000, 500, 1000], [1000, 2100, 500, 1000]]

    fea2 = [[100,110,40,80],[150,110,180,80],[350,110,120,90],[500,110,100,100],[630,110,70,90],[740,110,60,80],
    [120,310,140,100],[280,310,60,80],[370,310,80,80],[480,310,80,80],[580,310,100,100],[700,310,100,100],
    [100,490,80,80],[200,490,180,80],[400,490,120,90],[540,490,120,90],[690,490,40,40],[760,490,40,40],
    [140,690,70,70],[240,690,140,100],[400,690,70,80],[500,690,100,100],[630,690,70,80],[720,690,80,70],
    [1000,110,180,80],[1200,110,100,100],[1330,110,180,80],[1540,110,40,40],
    [1000,310,80,80],[1110,310,60,80],[1200,310,100,100],[1320,310,180,80],[1520,310,60,80],
    [1000,490,120,90],[1140,490,60,80],[1220,490,100,100],[1340,490,120,90],[1500,490,80,80],
    [1000,690,160,90],[1200,690,100,100],[1320,690,80,80],[1420,690,80,80],[1520,690,60,80]]

class ExpSetting:

    

    @staticmethod
    def getBasicMap(width = 3000, height = 3000, feature = Feas.fea1):
        map = Map2D(width, height)
        for i in range(len(feature)):
            map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, feature[i]))
        return map
    
    @staticmethod
    def getBasicRadar():
        radar = Radar2D([0, math.pi], 510, 5600, 1, 5)
        return radar