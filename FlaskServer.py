# encoding=utf-8

from flask import Flask
from flask import request
from flask import Response
import os
import cv2
import json
import sys
import time

from ColorDescriptor import ColorDescriptor
from IndexImage import IndexImage
from Searcher import Searcher
from Tools import Tools

indexPath = 'statics/indexOfImage/index.csv'
uploadImagePath = 'statics/upload_pics/'
cd = ColorDescriptor((8, 12, 3))
index = IndexImage(indexPath,cd)
searcher = Searcher(indexPath)


def saveImage(uploaded_img,path):
    print "保存到本地"
    filename = os.path.basename(uploaded_img.filename)
    name,ext=os.path.splitext(filename)
    ext = ext.lower()
    standard_type = ('.png', '.jpg', '.bmp', '.jpeg')
    if ext not in standard_type:
        print "图片格式错误"
        return 0
    else:
        # 检查图片格式、保存到本地(服务器)
        f_out = open(path, 'wb')
        uploaded_image_buffer = uploaded_img.read()
        f_out.write(uploaded_image_buffer)
        f_out.close()

        #保存完了顺便建立索引
        index.addIndexForImage(path)
        print "图片顺利保存并建立索引"
        return 1

# 创建Flask实例
app = Flask(__name__)

# 动态路由
@app.route('/controller/<params>')
def controller(params):
    # 重新索引
    if params == "reindex":
        print "reindex ING.."
        index.createIndexOfdatasetPath(uploadImagePath)
        print "done"
        return "done"
    # 把文件名中含有的逗号替换成下划线
    elif params == "replaceSpecialName":
        Tools.replaceSpecialName(uploadImagePath)
        return "done"
    # 清理CSV文件,即去重
    elif params == "cleanCSV":
        Tools.removeTheSameNameOfCSV(indexPath)
        return "BUG not fixed yet"
    else:
        return "nothing happened"

# 动态路由返回图片用
@app.route('/statics/upload_pics/<image_name>')
def showImage(image_name):
    img = open(uploadImagePath+image_name,'rb')
    resp = Response(img,mimetype="image/jpeg")
    return resp

@app.route('/image/<image_name>')
def image(image_name):
    img = open(uploadImagePath+image_name,'rb')
    resp = Response(img,mimetype="image/jpeg")
    return resp

# 静态路由
@app.route('/uploaddataset', methods=['GET','POST'])
def uploaddataset():
    if request.method == 'POST':
        # 获取上传的图片并预处理文件名
        uploaded_img = request.files['image']
        # 处理文件名
        filename = os.path.basename(uploaded_img.filename)
        if "," in filename:
            filename = filename.replace(",","_")
        filename = filename.lower()
        path = uploadImagePath+filename
        # 保存到本地
        if saveImage(uploaded_img,path):
            return "success"
        else:
            return "wrong format"
    else:
        print "visiting uploaddataset with GET"
        return "visiting uploaddataset with GET"

@app.route('/searchimage',methods=['GET','POST'])
def searchiamge():
    if request.method == 'POST':
        print "POST进入serachimage"
        # 获取上传的图片并预处理文件名
        target_img = request.files['image']
        # 处理文件名
        filename = os.path.basename(target_img.filename)
        if "," in filename:
            filename = filename.replace(",","_")
        filename = filename.lower()
        path = uploadImagePath + filename
        # 保存到本地
        if saveImage(target_img,path):
            # 可以从CSV中拿最新的一个就是这个图的特征
            # 也可以再用Descriptor描述一遍
            img = cv2.imread(path)
            features = cd.describe_color(img)
            results = searcher.search(features)
            # 这个results里面存储的是 score和resultID
            # 保存一下所有的图片地址,返回过去
            resultImgPath = []
            for(score,resultID) in results:
                # print resultID
                resultImgPath.append(uploadImagePath+resultID)
            print "search的结果是:"
            print resultImgPath
            return json.dumps(resultImgPath)
        else:
            print "wrong format"
            return "wrong format"
    else:
        return "visiting searchiamge with GET"

if __name__ == '__main__':
    app.run(host='0.0.0.0')

