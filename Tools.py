# encoding=utf-8
import os
import csv


class Tools(object):
    @staticmethod
    # path 是待清理的文件夹,会把文件夹中的所有含逗号的文件名替换,逗号换成下划线
    def replaceSpecialName(path):
        filelist = os.listdir(path)
        for files in filelist:
            originalDir = os.path.join(path, files)
            if os.path.isdir(originalDir):
                # 如果是文件夹就跳过
                continue
            name = os.path.splitext(files)[0]  # 文件名
            ext = os.path.splitext(files)[1]  # 后缀名
            if "," in name:
                name = name.replace(",", "_")
                newDir = os.path.join(path, name + ext)
                os.rename(originalDir, newDir)

    @staticmethod
    # path 是CSV文件的路径,去重
    def removeTheSameNameOfCSV(path):
        print "not finished yet"
        # with open(path) as f:
        #     # 初始化 CSV reader
        #     reader = csv.reader(f)
        #     output = open('statics/indexTemp.csv',"w")
        #
        #     # 先转换成list
        #     tempList = []
        #     for row in reader:
        #         tempList.extend(row)
        #         tempList.extend('\n')
        #     print tempList
        #     # List 去重
        #     resultList = tempList
        #     # for i in range(len(tempList)-1,0,-1):
        #     #     for j in range(len(tempList)-1,i,-1):
        #     #         print i,j
        #     #         if tempList[i] == tempList[j]:
        #     #             print "remove now"
        #     #             print j
        #     #             resultList.pop(j)
        #     # print resultList
        #     # 把resultList 写入 indexTemp.csv
        #     for row in resultList:
        #         output.write(row)
        #     output.close()
        #     f.close()

