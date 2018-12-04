# -*- coding: UTF-8 -*-

class Sum:
    @staticmethod
    def getSum(arr, start, end):
        sum = 0.0
        for i in range(start, end):
            sum += arr[i]
        return sum

class Avg:

    @staticmethod
    def getXAvg(arr, start, end):
        sum = Sum.getSum(arr, start, end)
        return sum / (end - start)
    
    @staticmethod
    def getRadarAvg(radar_data, start, end):
        xs = [x[0] for x in radar_data]
        ys = [y[1] for y in radar_data]
        return [Avg.getXAvg(xs, start, end), Avg.getXAvg(ys, start, end)]



class Normal:

    @staticmethod
    def normalParam(params, start, end):
        sum = Sum.getSum(params, start, end)
        for i in range(start, end):
            params[i] = params[i] / sum