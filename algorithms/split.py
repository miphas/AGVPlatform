# -*- coding: UTF-8 -*-

import math

class Split:

    @staticmethod
    def getSingleSplitPoint(radar_data, oneRange):
        idxA = oneRange[0]
        idxB = oneRange[1] - 1
        dx = radar_data[idxB][0] - radar_data[idxA][0]
        dy = radar_data[idxB][1] - radar_data[idxA][1]
        la = [dx, dy]
        dis_val = 0
        idx_val = oneRange[0]
        for i in range(oneRange[0], oneRange[1]):
            dis = Split.getDistanceByLine(radar_data[i], la, radar_data[idxA][0], radar_data[idxA][1])
            if dis_val < dis:
                dis_val = dis
                idx_val = i
        return idx_val

    # get distance between radar point and corresponding point on la
    @staticmethod
    def getDistanceByLine(rp, la, x1, y1):
        rate = (la[0] * (rp[0] - x1) + la[1] * (rp[1] - y1)) / float(la[0] * la[0] + la[1] * la[1])
        cur_x = x1 + rate * la[0]
        cur_y = y1 + rate * la[1]
        dx = rp[0] - cur_x
        dy = rp[1] - cur_y
        return math.sqrt(dx * dx + dy * dy)
    

    @staticmethod
    def getAroundIdx(radar_data, center_idx, dis):
        ret = []
        i = center_idx
        while 0 <= i and Split.getDistanceByPoint(radar_data[center_idx], radar_data[i]) < dis:
            i -= 1
        ret.append(i)
        i = center_idx
        while i < len(radar_data) and Split.getDistanceByPoint(radar_data[center_idx], radar_data[i]) < dis:
            i += 1
        ret.append(i)
        return ret

    @staticmethod
    def getDistanceByPoint(pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return math.sqrt(dx * dx + dy * dy)