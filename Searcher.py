# encoding=utf-8
import numpy as np
import csv


class Searcher:
    def __init__(self, indexPath):
        self.indexPath = indexPath

    # histA histB -- 用来比较的两个直方图
    # method -- 默认是0,使用卡方距离; 1, 使用欧氏距离; 2, 使用余弦距离
    # eps -- 一个极小值,避免除零错误
    @staticmethod
    def distance(histA, histB, method=0, eps=1e-10):
        # d 默认使用 卡方距离 来初始化
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                              for (a, b) in zip(histA, histB)])
        if method == 0:
            # 卡方 chi-square
            d = d

        if method == 1:
            # 欧氏距离
            d = np.sum([(a-b)**2
                        for (a,b) in zip(histA,histB)]) ** 0.5
        if method == 2:
            # 余弦距离
            temp1,temp2,temp3 = eps
            for i in range(len(histA)):
                temp1 += histA[i] * histB[i]
                temp2 += histA[i] * histA[i]
                temp3 += histB[i] * histB[i]
            d = temp1/((temp2*temp3)**0.5)
        return d

    # queryFeatures -- 目标图像(提交的图像)的特征
    # limit --  限定返回图像的个数 (默认为10个)
    # 返回的result如下:
    # [(1.2541891457949072e-12, 'UNADJUSTEDNONRAW_thumb_1e.jpg'), ...]
    def search(self, queryFeatures, limit=10):
        results = {}
        with open(self.indexPath) as f:
            # 初始化 CSV reader
            reader = csv.reader(f)
            for row in reader:
                features = [float(x)
                            for x in row[1:]]
                d = self.distance(features, queryFeatures)
                results[row[0]] = d
            f.close()

        # 根据distance排个序,越相似的就在前面
        results = sorted([(v, k)
                          for (k, v) in results.items()])
        print "results is \n",results
        return results[:limit]

