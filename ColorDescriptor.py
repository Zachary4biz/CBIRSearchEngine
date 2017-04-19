# encoding=utf-8

import numpy as np
import cv2
import skimage
from skimage.feature import local_binary_pattern as lbp
class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins

    # 均衡化
    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    # 使用颜色描述子
    def describe_color(self, image):
        # 转换到HSV颜色空间
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # features用来量化图像
        features = []

        # image.shape是一个数组,前两项分别是图像的高和宽
        (h, w) = image.shape[:2]
        # centerX和centerY
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        # 绘制代表中间部分的椭圆
        (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        # 获取中心椭圆的颜色直方图
        hist = self.histogram(image, ellipMask)
        features.extend(hist)

        # 把图像分割成除了中心椭圆的四个角
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]
        for (startX, endX, startY, endY) in segments:
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            # 要把椭圆的部分从cornerMask挖去
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            # 获取每个部分的颜色直方图,并保存到features数组中
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        return features

    # 使用纹理描述子(LBP)
    def describe_texture(self, image):
        # LBP参数
        radius = 3
        n_points = 8 * radius
        # 建立LBP
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        lbp_image = lbp(image,n_points,radius)
        cv2.imwrite("statics/indexOfImage/test.jpg",lbp_image)
        return image


if __name__ == '__main__':
    cd = ColorDescriptor((8,12,3))
    image = cv2.imread("/Users/zac/Desktop/temp.jpg")
    cd.describe_texture(image)
    print "done"
