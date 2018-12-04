# -*- coding: UTF-8 -*-

import math

class DBSCAN:

    # get break points from scan data
    @staticmethod
    def getBreakPoints(radar_data, radar_pos):
        ret_pos = [0]
        for i in range(1, len(radar_data)):
            sx = radar_data[i][0] - radar_pos[0]
            sy = radar_data[i][1] - radar_pos[1]
            thr = math.sqrt(sx * sx + sy * sy) * 0.04
            #thr = 90
            dx = radar_data[i][0] - radar_data[i - 1][0]
            dy = radar_data[i][1] - radar_data[i - 1][1]
            dis = math.sqrt(dx * dx + dy * dy)
            if dis > thr:
                ret_pos.append(i)
        return ret_pos
    
    # get feature range with scan data
    @staticmethod
    def getFeatureRange(radar_data, radar_pos):
        ret_range = []
        bps = DBSCAN.getBreakPoints(radar_data, radar_pos)
        for i in range(0, len(bps) - 1):
            if radar_data[bps[i]][2] == 0:
                continue
            ret_range.append([bps[i], bps[i + 1]])
        if radar_data[bps[len(bps) - 1]][2] != 0:
            ret_range.append([bps[len(bps) - 1][2], len(radar_data)])
        return ret_range




# test break point method
if __name__ == '__main__':
    # import files
    import sys
    sys.path.append('..')
    from figure.mapFigure import MapFigure
    from map.map2D import Map2D
    from sensor.radar2D import Radar2D
    from split import Split
    # 
    map = Map2D(2000, 2000)
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [100, 500, 500, 1400]))
    map.addFeature(Map2D.Feature(Map2D.Feature.rectangle, [1400, 600, 600, 1200]))

    radar = Radar2D([0, math.pi], 510, 5600, 1, 5)
    radar_pos = [1000, 0, 0]
    radar_data = radar.getMeasureData(map, radar_pos)

    bps = DBSCAN.getBreakPoints(radar_data, radar_pos)
    rag = DBSCAN.getFeatureRange(radar_data, radar_pos)
    for i in range(len(radar_data)):
        print i, radar_data[i]
    print bps
    print rag

    p1 = Split.getSingleSplitPoint(radar_data, rag[0])
    print p1
    p2s = Split.getAroundIdx(radar_data, p1, 25)


    xs = [x[0] for x in radar_data]
    ys = [x[1] for x in radar_data]

    fig = MapFigure(map)
    fig.drawMapByFeatures()

    colors = ['b.', 'r.', 'g.']
    for i in range(len(rag)):
        s = rag[i][0]
        e = rag[i][1]
        fig.drawRadarPoints(xs[s : e], ys[s : e], colors[i])
    fig.drawRadarPoints(xs[p1], ys[p1], 'wo')
    fig.drawRadarPoints(xs[p2s[0]], ys[p2s[0]], 'wo')
    fig.drawRadarPoints(xs[p2s[1]], ys[p2s[1]], 'wo')

    fig.setXYLim(0, 2000, 0, 2000)
    fig.showFigure()
