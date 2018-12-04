# -*- coding: UTF-8 -*-

import numpy as np

class LeastSquare:

    @staticmethod
    def genPhiAndY(radar_data, start, end):
        num = end - start
        phi = np.zeros((num, 2))
        y_val = np.zeros((num, 1))
        for i in range(num):
            pos = i + start
            phi[i][0] = 1
            phi[i][1] = radar_data[pos][0]
            y_val[i][0] = radar_data[pos][1]
        phi = np.mat(phi)
        y_val = np.mat(y_val)
        return phi, y_val
    
    @staticmethod
    def genPVal(phi):
        p_val = phi.T * phi
        return p_val.I

    @staticmethod
    def normalCal(radar_data, start, end):
        phi, y_val = LeastSquare.genPhiAndY(radar_data, start, end)
        p_val = LeastSquare.genPVal(phi)
        theta = p_val * phi.T * y_val
        print theta, p_val, len(p_val)
        return theta, p_val
    
    # 最小二乘方法初始化
    def __init__(self, theta, p_val):
        self.theta = theta
        self.p_val = p_val
    
    def recursiveCal(self, radar_data, start, end, rate = 1.0):
        for i in range(start, end):
            phi, y_val = LeastSquare.genPhiAndY(radar_data, i, i + 1)
            g_val = (self.p_val * phi.T) / (rate + phi * self.p_val * phi.T)
            p_val = (self.p_val - g_val * phi * self.p_val) * (1.0 / rate)
            theta = self.theta + g_val * (y_val - phi * self.theta)
            self.p_val = p_val
            self.theta = theta
        return self.theta, self.p_val
    


a = np.zeros((2, 1))
a = np.mat(a)

print a