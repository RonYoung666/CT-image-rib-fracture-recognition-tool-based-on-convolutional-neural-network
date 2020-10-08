#coding=utf-8
import os
import shutil
import random

trainpath = "D:/CTrfd/TensorFlow/workspace/training_demo/images/train/"
testpath = "D:/CTrfd/TensorFlow/workspace/training_demo/images/test/"

def split(jpgpath,xmlpath):
    patient_list = os.listdir(xmlpath)
    for patient in patient_list:
        print(jpgpath + patient)
        xml_list = os.listdir(xmlpath + patient)
        for xml in xml_list:
            jpg = os.path.splitext(xml)[0] + '.jpg'
            xmldata = xmlpath + patient + '/' + xml
            jpgdata = jpgpath + patient + '/' + jpg
            if random.random() < 0.9: #0.9的概率复制到train文件夹
                shutil.copy(xmldata, trainpath)
                shutil.copy(jpgdata, trainpath)
            else: #0.1的概率复制到test文件夹
                shutil.copy(xmldata, testpath)
                shutil.copy(jpgdata, testpath)

if __name__ == "__main__":
    existtrain = os.path.exists(trainpath)
    existtest = os.path.exists(testpath)
    if not existtrain:
        os.makedirs(trainpath)
        print("create " + trainpath)
    if not existtest:
        os.makedirs(testpath)
        print("create " + testpath)

    jpgpath = "D:/CTrfd/TensorFlow/data/jpgs/"
    mrdjpgpath = "D:/CTrfd/TensorFlow/data/mrdjpgs/"
    xmlpath = "D:/CTrfd/TensorFlow/data/xmls/"
    mrdxmlpath = "D:/CTrfd/TensorFlow/data/mrdxmls/"
    split(jpgpath,xmlpath)
    split(mrdjpgpath,mrdxmlpath)
