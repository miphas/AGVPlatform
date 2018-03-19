# -*- coding: UTF-8 -*-

import math

# Import import other files
import sys
sys.path.append('..')

# Import setting and map2D
from map.map2D import Map2D
from dataFactory.randomNum import RandomNum

class Radar2D:

    # Radar2D init laser parameter
    # ------------------------------------------------------------------------
    # angles: the start and end of laser radar, exp[0, math.pi]
    # lines:  the total num of measurement lines in range
    # distance: the farthest distance the radar can measure
    # size: each unit contains size mm
    # sd: the standard deviation(标准差) of each measure at distance of 1000mm
    # failureVal: the value of measurement when failure
    # ------------------------------------------------------------------------
    def __init__(self, angles, lines, distance, size = 1, sd = 10, dysd = True, failureVal = 0):
        self.angles = angles
        self.lines = lines
        self.ang_step = (self.angles[1] - self.angles[0]) / float(lines)
        self.distance = distance
        self.size = size
        self.sd = sd
        self.dysd = dysd
        self.failureVal = failureVal
    
    # Radar2D get measure data from map
    # ------------------------------------------------------------------------
    # radarPos: the position of radar in map
    # dysd: enable the adjustment of sd with distance
    # ------------------------------------------------------------------------
    def getMeasureData(self, map, radarPos):
        ret_pos = []
        seq_nor = RandomNum.createNormal(0, self.sd, self.lines)
        self.__traverseAllLines(self.__getLinePoint, 
            cur_pos = radarPos, ret_pos = ret_pos, map = map, seq_nor = seq_nor)
        return ret_pos

    # __Map2D traverse all the measurement lines
    def __traverseAllLines(self, func, **args):
        for i in range(self.lines):
            cur_ang = self.angles[0] + i * self.ang_step
            func(cur_ang, i, **args)
    
    # __Map2D get each point in measurement line
    def __getLinePoint(self, cur_ang, cur_i, cur_pos, ret_pos, map, seq_nor):
        px = math.cos(cur_ang + cur_pos[2])
        py = math.sin(cur_ang + cur_pos[2])
        dis = self.__getFirstOcc(map, cur_pos, px, py)
        if dis != -1:
            if self.dysd:
                seq_nor[cur_i] *= dis * self.size / 1000.0
            cx, cy = self.__getCurXY(cur_pos, px, py, dis + seq_nor[cur_i])
            if map.checkInMap(cx, cy):
                ret_pos.append([cx, cy, int(dis + seq_nor[cur_i])])
                return
        cx, cy = self.__getCurXY(cur_pos, px, py, self.failureVal)
        ret_pos.append([cx, cy, self.failureVal])

    # __Map2D getCurXY with distance
    def __getCurXY(self, cur_pos, px, py, dis):
        cx = int(cur_pos[0] + dis * px)
        cy = int(cur_pos[1] + dis * py)
        return cx, cy
    
    # __Map2D get first occupied grid in map
    def __getFirstOcc(self, map, cur_pos, px, py):
        for i in range(self.distance):
            cx, cy = self.__getCurXY(cur_pos, px, py, i)
            if not map.checkInMap(cx, cy):
                return -1
            if map.s_grid[cx][cy] == Map2D.occupied:
                return i
        return -1
