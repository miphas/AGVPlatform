# -*- coding: UTF-8 -*-

import math
import sys
sys.path.append('..')
from map.map2D import Map2D

class ObjModel:

    def __init__(self, feas, width, height):
        self.feas = feas
        # 创建模型占用地图
        self.map = Map2D(width, height)
        # 默认角度设定为0
        self.angle = 0
        self.__initFeasOnMap()
    
    def getRotateModel(self, angle):
        w, h = self.map.m_width, self.map.m_height
        #print w, h
        l = max(w, h) + 100
        l2 = 2 * l
        n_map = Map2D(l2, l2)
        for i in range(0, w):
            for j in range(0, h):
                dis = math.sqrt(i ** 2 + j ** 2)
                ang = 0
                if dis != 0:
                    ang = math.acos(i / dis) + angle / 180.0 * math.pi
                nx = dis * math.cos(ang)
                ny = dis * math.sin(ang)
                #print nx, ny
                n_map.setValInMap(l + nx, l + ny, self.map.s_grid[i][j]) #self.map.s_grid[i][j]
        return n_map


    
    def __initFeasOnMap(self):
        for f in self.feas:
            self.map.addFeature(f)
            

class Models:
    carModel = [Map2D.Feature(Map2D.Feature.ellipse, [20, 20, 40, 40, 0]), # 车尾
                Map2D.Feature(Map2D.Feature.rectangle, [20, 0, 130, 20, 0]),
                Map2D.Feature(Map2D.Feature.ellipse, [150, 20, 40, 40, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [0, 20, 170, 25, 0]), 
                Map2D.Feature(Map2D.Feature.ellipse, [45, 338, 90, 74, 0]), #车头
                Map2D.Feature(Map2D.Feature.ellipse, [125, 338, 90, 74, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [45, 338, 80, 37, 0]), 
                Map2D.Feature(Map2D.Feature.erase, [0, 280, 170, 58, 0]), 
                Map2D.Feature(Map2D.Feature.rectangle, [0, 320, 170, 18, 0]), 
                Map2D.Feature(Map2D.Feature.rectangle, [0, 85, 20, 195, 0]), # 中间
                Map2D.Feature(Map2D.Feature.rectangle, [150, 85, 20, 195, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [10, 45, 10, 40, 0]), #车轮
                Map2D.Feature(Map2D.Feature.rectangle, [150, 45, 10, 40, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [20, 65, 130, 4, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [10, 280, 10, 40, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [150, 280, 10, 40, 0]),
                Map2D.Feature(Map2D.Feature.rectangle, [20, 300, 130, 4, 0]),]