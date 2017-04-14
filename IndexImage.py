# encoding=utf-8
from ColorDescriptor import ColorDescriptor
import glob
import cv2
import sys

# cd = ColorDescriptor((8, 12, 3))
class IndexImage:
    # index -- 存放 图片集做好的特征索引 的路径
    def __init__(self, index, cd):
        self.index = index
        self.cd = cd

    # 对某个目录(dataset)里所有的图片做一个索引
    # 这里特意使用了"w" 写模式 打开路径,这样可以自动清空上一次的索引数据
    def createIndexOfdatasetPath(self,dataset):
        output = open(self.index,"w")

        allImgaePath = []
        allImgaePath.extend(glob.glob(dataset+"*.png"))
        allImgaePath.extend(glob.glob(dataset+"*.jpg"))
        counter = 0
        for imagePath in allImgaePath:
            imageID = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            features = self.cd.describe(image)
            features = [str(f) for f in features]
            output.write("%s,%s\n" % (imageID,",".join(features)))
            counter += 1
            sys.stdout.write("\r%d/%d"%(counter,len(allImgaePath)))
            sys.stdout.flush()
        output.close()

    # 对某个图片做索引
    # 使用追加模式
    def addIndexForImage(self,imagePath):
        output = open(self.index,'a')
        imageID = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        features = self.cd.describe(image)
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imageID,",".join(features)))
        output.close()
