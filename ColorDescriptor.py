# encoding=utf-8

import numpy as np
import cv2
from skimage.feature import local_binary_pattern as lbp
from skimage.exposure import histogram as ske_histogram
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt



def calcAndDrawHist(image, color):
    hist= cv2.calcHist([image], [0], None, [256], [0.0,255.0])
    cv2.normalize(hist,hist).flatten()
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256,256,3], np.uint8)
    hpt = int(0.9* 256)

    for h in range(256):
        intensity = int(hist[h]*hpt/maxVal)
        cv2.line(histImg,(h,256), (h,256-intensity), color)

    return histImg
def drawHist(target_hist):
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(target_hist)
    histImg = np.zeros([256,256,3], np.uint8)
    hpt = int(0.9* 256)

    for h in range(256):
        intensity = int(target_hist[h]*hpt/maxVal)
        cv2.line(histImg,(h,256), (h,256-intensity), [0,0,255])

    return histImg

class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins

    # 计算并归一化
    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        # normalize 归一化
        # flatten 变成一维的,比如array([[1,2],[3,4]]) flatten就是array([1,2,3,4])
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
        radius = 1
        n_points = 8 * radius
        # 建立LBP
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        lbp_image = lbp(image,n_points,radius)

        # 统计图像的直方图
        max_bins = int(lbp_image.max() + 1)
        # hist size:256
        lbp_hist= np.histogram(lbp_image, normed=True, bins=max_bins, range=(0, max_bins))

        # print "lbp_hist is :"
        # print lbp_hist[0]
        # 发现lbp_hist比普通的hist要多一列其,lbp_hist[1]的内容是0~256,没必要,直接取它的[0]传去绘图就行了
        new_lbp_hist = lbp_hist[0]
        # print "numpy得到的lbp直方图是\n",new_lbp_hist
        # 归一化处理一下
        new_lbp_hist = cv2.normalize(new_lbp_hist,new_lbp_hist)
        # print "归一化之后的直方图是\n",new_lbp_hist


        # histImg = drawHist(new_lbp_hist)
        # cv2.imwrite("/Users/zac/Desktop/new_lbp_hist1_2.jpg",histImg)

        # cv2.imwrite("/Users/zac/Desktop/original_IMG_lbp_r2.jpg",lbp_image)
        #
        # lbpIMG = cv2.imread("/Users/zac/Desktop/original_IMG_lbp_r2.jpg")
        # histIMG = calcAndDrawHist(lbpIMG,[0,0,255])
        # cv2.imwrite("/Users/zac/Desktop/lbp_hist_flatten.jpg",histIMG)
        return new_lbp_hist


if __name__ == '__main__':
    cd = ColorDescriptor((8,12,3))
    # 纹理
    image = cv2.imread("/Users/zac/Desktop/bottle1_2.jpg")
    cd.describe_texture(image)
    # 颜色
    image_night = cv2.imread("/Users/zac/Desktop/original_IMG1.jpg")
    hist = cd.describe_color(image_night)


    print "done"
