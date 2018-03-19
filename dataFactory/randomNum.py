# -*- coding: UTF-8 -*-

import numpy as np

class RandomNum:
    
    # Create random number which obay the normal distribution
    @staticmethod
    def createNormal(avg, sigma, sampleNum):
        if sigma == 0:
            return np.zeros(sampleNum)
        np.random.seed()
        return np.random.normal(avg, sigma, sampleNum)


