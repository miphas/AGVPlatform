# -*- coding: UTF-8 -*-

import math
import time
import sys
sys.path.append('..')
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from dataFactory.randomNum import RandomNum
from figure.mapFigure import MapFigure
from map.map2D import Map2D

class Particle:

    def __init__(self, x, w):
        self.x = float(x)
        self.w = float(w)

class ParticleSet:

    def __init__(self, vals):
        self.pset = []
        p_weight = 1.0 / len(vals)
        for i in range(len(vals)):
            self.pset.append(Particle(vals[i], p_weight))
    
    def samplingSIS(self, num):
        weight_line = self.__getWeightLine()
        random_seqs = RandomNum.createRandom(num)
        n_pset = []
        for i in range(num):
            idx = self.__getIdxInLine(weight_line, random_seqs[i])
            n_pset.append(Particle(self.pset[idx].x, 1.0 / num))
        self.pset = n_pset
    def samplingLVS(self, num):
        weight_line = self.__getWeightLine()
        r = RandomNum.createRandom(1) * 1.0 / num
        n_pset = []
        r_per = 1.0 / num
        for i in range(num):
            idx = self.__getIdxInLine(weight_line, r)
            n_pset.append(Particle(self.pset[idx].x, 1.0 / num))
            r += r_per
        self.pset = n_pset
    def samplingVIS(self, num):
        weight_line = self.__getWeightLine()
        random_seqs = RandomNum.createRandom(num)
        n_pset = []
        for i in range(num):
            idx = self.__getIdxInLine(weight_line, random_seqs[i])
            n_pset.append(Particle(self.pset[idx].x, 1.0 / num))
            self.pset[idx].w -= 1.0 / num
            if self.pset[idx].w < 0:
                self.pset[idx].w = 0
            self.__refreshSeq()
        self.pset = n_pset


    
    def getCurrentVal(self):
        ans = 0.0
        for i in range(len(self.pset)):
            ans += self.pset[i].x * self.pset[i].w
        return ans
    
    def predictSeq(self, t, vts):
        vts = RandomNum.createNormal(0, 1, len(self.pset))
        for i in range(len(self.pset)):
            self.pset[i].x = PFSim.getNextX(t, self.pset[i].x, vts[i])
    
    def updateSeq(self, center):
        for i in range(len(self.pset)):
            self.pset[i].w = norm.pdf(center - math.pow(self.pset[i].x, 2) / 20.0)
            #print self.pset[i].w
        self.__refreshSeq()
    
    def getOccRoom(self):
        min_val = self.pset[0].x
        max_val = self.pset[0].x
        for i in range(1, len(self.pset)):
            min_val = min(min_val, self.pset[i].x)
            max_val = max(max_val, self.pset[i].x)
        ret = max(1, (max_val - min_val) * 100)
        return ret
    
    def __getWeightLine(self):
        weight_init = 0.0
        weight_line = []
        for i in range(len(self.pset)):
            weight_line.append(weight_init + self.pset[i].w)
            weight_init += self.pset[i].w
        return weight_line
    
    def __getIdxInLine(self, weight_line, val):
        for i in range(len(self.pset)):
            if weight_line[i] > val:
                return i
        return len(self.pset) - 1
    
    def __refreshSeq(self):
        sum = 0.0
        for i in range(len(self.pset)):
            sum += self.pset[i].w
        for i in range(len(self.pset)):
            self.pset[i].w /= sum

class PFSim:

    @staticmethod
    def getNextX(i, x, vt):
        ans = 0.5 * x + 25 * x / (1 + x * x) + 8 * math.cos(1.2 * i) + vt
        return ans

    @staticmethod
    def getSeqX(init_val, cnt):
        x = init_val
        vts = RandomNum.createNormal(0, 1, cnt)
        ret = np.zeros(cnt)
        for i in range(cnt):
            ret[i] = PFSim.getNextX(i, x, vts[i])
            x = ret[i]
        return ret
    
    @staticmethod
    def getSeqO(seqX):
        cnt = len(seqX)
        nts = RandomNum.createNormal(0, 1, cnt)
        ret = np.zeros(cnt)
        for i in range(cnt):
            ret[i] = 0.05 * math.pow(seqX[i], 2) + nts[i]
        return ret
    
    @staticmethod
    def getRMSE(seqX, seqOther):
        ans = 0.0
        for i in range(len(seqX)):
            ans += math.pow(seqX[i] - seqOther[i], 2)
        return math.sqrt(ans / len(seqX))
    
    @staticmethod
    def genNormalRan(cnt, num):
        ret = []
        for i in range(cnt):
            ret.append(RandomNum.createNormal(0, 1, num))
        return ret
    
    @staticmethod
    def genKLDNum(k):
        if k == 1:
            return 200
        k1 = k - 1
        param = k1 / 0.1
        val9 = 2.0 / (9.0 * k1)
        return int(param * math.pow(1 - val9 + math.sqrt(val9) * 2.35, 3))

def sim1(init_val):
    num = 60
    sam = 60
    seqX = PFSim.getSeqX(init_val, num)
    seqO = PFSim.getSeqO(seqX)

    rans = PFSim.genNormalRan(num, sam)

    # SIS
    seqR = [init_val]
    timeSIS = time.clock()
    pset = ParticleSet(np.linspace(-10, 10, 400))
    for i in range(1, len(seqX)):
        pset.samplingSIS(sam)
        pset.predictSeq(i, rans[i])
        pset.updateSeq(seqO[i])
        seqR.append(pset.getCurrentVal())
    timeSIS = time.clock() - timeSIS

    # LVS
    seqLVS = [init_val]
    timeLVS = time.clock()
    pset = ParticleSet(np.linspace(-10, 10, 400))
    for i in range(1, len(seqX)):
        pset.samplingLVS(sam)
        pset.predictSeq(i, rans[i])
        pset.updateSeq(seqO[i])
        seqLVS.append(pset.getCurrentVal())
    timeLVS = time.clock() - timeLVS

    # VIS
    seqVIS = [init_val]
    timeVIS = time.clock()
    pset = ParticleSet(np.linspace(-10, 10, 400))
    for i in range(1, len(seqX)):
        pset.samplingVIS(sam)
        pset.predictSeq(i, rans[i])
        pset.updateSeq(seqO[i])
        seqVIS.append(pset.getCurrentVal())
    timeVIS = time.clock() - timeVIS
    
    
    fig = MapFigure(Map2D(200, 200))
    index = np.arange(0, num, 1)
    print len(index), len(seqX)
    print PFSim.getRMSE(seqX, seqR)
    print PFSim.getRMSE(seqX, seqLVS)
    print PFSim.getRMSE(seqX, seqVIS)
    print timeSIS, timeLVS, timeVIS

    l1 = fig.drawRadarPoints(index, seqX, 'ro-')
    l2 = fig.drawRadarPoints(index, seqR, 'm<:', 1.5)
    l3 = fig.drawRadarPoints(index, seqLVS, 'c<:', 1.5)
    l4 = fig.drawRadarPoints(index, seqVIS, 'g*--', 1.5)
    plt.legend([l1, l2, l3, l4], [u'True', u'SIS', 'LVS', 'VIS'], loc = 'upper right')
    fig.setXYLabel(u'数据编号', u'距离/mm')
    #print seqR
    fig.showFigure()

#sim1(5)

# 自适应采样空间大小实验

def sim2(init_val):
    num = 20
    sam = 60
    seqX = PFSim.getSeqX(init_val, num)
    seqO = PFSim.getSeqO(seqX)

    rans = PFSim.genNormalRan(num, sam)

    # SIS-KLD-FIX
    seqFIX1 = [init_val]
    timeSIS = time.clock()
    nums1 = []
    pset = ParticleSet(np.linspace(-20, 20, 4000))
    for i in range(1, len(seqX)):
        toSam = PFSim.genKLDNum(max(1, pset.getOccRoom() / 80))
        nums1.append(toSam)
        pset.samplingSIS(toSam)
        pset.predictSeq(i, rans[i])
        pset.updateSeq(seqO[i])
        seqFIX1.append(pset.getCurrentVal())
    timeSIS = time.clock() - timeSIS

    # SIS-KLD-FIX
    seqFIX2 = [init_val]
    timeFIX2 = time.clock()
    nums2 = []
    pset = ParticleSet(np.linspace(-20, 20, 4000))
    for i in range(1, len(seqX)):
        toSam = PFSim.genKLDNum(max(1, pset.getOccRoom() / 240))
        nums2.append(toSam)
        pset.samplingSIS(toSam)
        pset.predictSeq(i, rans[i])
        pset.updateSeq(seqO[i])
        seqFIX2.append(pset.getCurrentVal())
    timeFIX2 = time.clock() - timeFIX2

    # SIS-KLD-ADA
    seqADA = [init_val]
    timeADA = time.clock()
    nums3 = []
    pset = ParticleSet(np.linspace(-20, 20, 4000))
    for i in range(1, len(seqX)):
        ori = pset.getOccRoom() / 200
        toSam = PFSim.genKLDNum(min(7, ori))
        nums3.append(toSam)
        pset.samplingSIS(toSam)
        pset.predictSeq(i, rans[i])
        pset.updateSeq(seqO[i])
        seqADA.append(pset.getCurrentVal())
    timeADA = time.clock() - timeADA

    
    fig = MapFigure(Map2D(200, 200))
    index = np.arange(0, num, 1)
    print len(index), len(seqX)
    print nums1
    print nums2
    print nums3
    print timeSIS, PFSim.getRMSE(seqX, seqFIX1)
    print timeFIX2, PFSim.getRMSE(seqX, seqFIX2)
    print timeADA, PFSim.getRMSE(seqX, seqADA)

    l1 = fig.drawRadarPoints(index, seqX, 'ro-')
    l2 = fig.drawRadarPoints(index, seqFIX1, 'm<:', 1.5)
    l3 = fig.drawRadarPoints(index, seqFIX2, 'bd:', 1.5)
    l4 = fig.drawRadarPoints(index, seqADA, 'g*--', 1.5)
    plt.legend([l1, l2, l3, l4], [u'True', u'FIX1', 'FIX2', 'ADA'], loc = 'upper right')
    fig.setXYLabel(u'数据编号', u'距离/mm')
    #print seqR
    fig.showFigure()
#sim2(0)

# 画自适应大小的粒子数曲线
n_x = np.arange(0, 20, 1)
n_fix1 = [2000, 752, 592, 456, 571, 556, 436, 179, 159, 165, 583, 547, 188, 153, 181, 584, 608, 440, 178, 180]
n_fix2 = [2000, 317, 237, 193, 241, 230, 186, 69, 71, 83, 247, 245, 75, 47, 70, 252, 240, 77, 60, 73]
n_ada = [2000, 170, 170, 170, 170, 170, 170, 98, 86, 102, 170, 170, 87, 84, 96, 170, 170, 79, 81, 71]

def drawPNum():
    fig = MapFigure(Map2D(200, 200))
    l1 = fig.drawRadarPoints(n_x, n_fix1, 'm-s')
    l2 = fig.drawRadarPoints(n_x, n_fix2, 'b--*')
    l3 = fig.drawRadarPoints(n_x, n_ada, 'g:o', 1.5)
    plt.legend([l1, l2, l3], [u'FIX1', u'FIX2', 'ADA'], loc = 'upper right')
    fig.setXYLabel(u'数据编号', u'粒子数/个')
    fig.showFigure()
#drawPNum()
def getAvg(nums, add_val):
    for i in range(len(nums)):
        add_val += nums[i]
    add_val /= len(nums)
    print add_val
getAvg(n_fix1, -2000)
getAvg(n_fix2, -2000)
getAvg(n_ada, -2000)


# 超声波、激光雷达定位误差与栅格大小关系
x = [4, 16, 32, 64]
yLaser = [3.88, 5, 9.4, 18.88]
ySonic = [7.5, 8.05, 11.94, 25.55]
eLaser = [0.33, 0.55, 0.88, 1.52]
eSonic = [0.69, 0.694, 1.35, 1.66]
def drawSensorLocErr():
    fig = MapFigure(Map2D(200, 200))
    l1 = fig.drawErrorBar(x, yLaser, eLaser, 'm-s')
    l2 = fig.drawErrorBar(x, ySonic, eSonic, 'b--o')
    fig.setXYLabel(u'栅格单元/cm', u'平均定位误差/cm')
    fig.setXYLim(0, 70, 0, 35)
    plt.legend([l1, l2], [u'LaserRad', u'SonicSen'], loc = 'upper right')
    fig.showFigure()
# drawSensorLocErr()

x = [4, 8, 16, 32, 48, 64]
def drawParticleSize():
    y = []
    for i in range(len(x)):
        y.append(PFSim.genKLDNum(6400 / x[i]))
    fig = MapFigure(Map2D(200, 200))
    l = fig.drawRadarPoints(x, y, 'bo-')
    fig.setXYLabel(u'栅格单元/cm', u'平均采样数/个')
    #plt.legend([l], [u'KLD'], loc = 'upper right')
    fig.showFigure()
#drawParticleSize()

